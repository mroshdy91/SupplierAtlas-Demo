"""Personal bearer credentials and atomic, durable fixed-window allowances.

Email is unverified metadata. It cannot authenticate or recover a credential.
Only digests are stored. Signed random tokens reject guesses before database IO.
"""
import hashlib
import hmac
import json
import os
import re
import secrets
import sqlite3
import time
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path


@dataclass(frozen=True)
class Limits:
    account_daily: int = 100
    account_minute: int = 20
    global_daily: int = 1000
    global_monthly: int = 10000
    http_daily: int = 3000
    http_monthly: int = 20000
    signup_daily: int = 20
    signup_monthly: int = 200
    accounts: int = 200

    @classmethod
    def from_env(cls):
        values = {name: int(os.getenv("SUPPLIER_ATLAS_LIMIT_" + name.upper(), value))
                  for name, value in asdict(cls()).items()}
        if any(value < 1 for value in values.values()):
            raise ValueError("Access limits must be positive integers")
        return cls(**values)


class AccessError(Exception):
    def __init__(self, code, status=429, retry_after=60):
        self.code, self.status, self.retry_after = code, status, max(1, int(retry_after))
        super().__init__(code)


class SQLiteAccessStore:
    """Durable local development store. Do not place it on Cloud Run scratch disk."""
    def __init__(self, path):
        self.path = str(path)
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        with sqlite3.connect(self.path) as db:
            db.execute("CREATE TABLE IF NOT EXISTS access_state (id TEXT PRIMARY KEY, value TEXT NOT NULL)")

    def transact(self, keys, operation):
        with sqlite3.connect(self.path, timeout=10) as db:
            db.execute("BEGIN IMMEDIATE")
            states = {}
            for key in keys:
                row = db.execute("SELECT value FROM access_state WHERE id=?", (key,)).fetchone()
                states[key] = json.loads(row[0]) if row else {}
            before = json.dumps(states, sort_keys=True)
            result = operation(states)
            if json.dumps(states, sort_keys=True) != before:
                for key, value in states.items():
                    db.execute("INSERT OR REPLACE INTO access_state VALUES (?,?)", (key, json.dumps(value)))
            return result


class FirestoreAccessStore:
    """Private server-only documents; ADC credentials, no browser database access."""
    def __init__(self, project, credentials=None, collection="supplieratlas_access"):
        from google.cloud import firestore
        self.client = firestore.Client(project=project, credentials=credentials)
        self.collection = self.client.collection(collection)

    def transact(self, keys, operation):
        from google.api_core.exceptions import Aborted
        from google.cloud import firestore
        refs = {key: self.collection.document(key) for key in keys}

        @firestore.transactional
        def run(transaction):
            states = {key: ref.get(transaction=transaction, timeout=5, retry=None).to_dict() or {}
                      for key, ref in refs.items()}
            before = {key: json.dumps(value, sort_keys=True) for key, value in states.items()}
            result = operation(states)
            for key, value in states.items():
                if json.dumps(value, sort_keys=True) != before[key]:
                    transaction.set(refs[key], value)
            return result

        # The SDK retries commit contention, but a transaction read can also abort.
        # Retry the entire transaction in that case; never retry an uncertain commit.
        for attempt in range(3):
            try:
                return run(self.client.transaction(max_attempts=3))
            except Aborted:
                if attempt == 2:
                    raise
                time.sleep(0.05 + secrets.randbelow(100) / 1000)


def digest(value):
    return hashlib.sha256(value.encode()).hexdigest()


def periods(now):
    date = datetime.fromtimestamp(now, UTC)
    next_month = datetime(date.year + (date.month == 12), date.month % 12 + 1, 1, tzinfo=UTC)
    return {"minute": (int(now // 60), int(now // 60 + 1) * 60),
            "day": (date.strftime("%Y-%m-%d"), int(now // 86400 + 1) * 86400),
            "month": (date.strftime("%Y-%m"), int(next_month.timestamp()))}


def count(state, name, period):
    value = state.get(name, {})
    return value.get("used", 0) if value.get("period") == period[0] else 0


def increment(state, name, period):
    state[name] = {"period": period[0], "used": count(state, name, period) + 1}


def exhausted(state, name, period, limit, now):
    if count(state, name, period) >= limit:
        return AccessError(name + "_limit", retry_after=period[1] - now)
    return None


class AccessService:
    def __init__(self, store, signing_key, owner_token=None, limits=None, clock=time.time):
        if len(signing_key) < 32:
            raise ValueError("Access signing key must have at least 32 characters")
        self.store, self.key, self.owner_token = store, signing_key.encode(), owner_token
        self.limits, self.clock = limits or Limits(), clock
        self.global_block_until = 0

    def signature(self, payload):
        return hmac.new(self.key, ("supplieratlas-access-v1:" + payload).encode(), hashlib.sha256).hexdigest()

    def new_token(self):
        payload = "sat_" + secrets.token_hex(32)
        return payload + "." + self.signature(payload)

    def token_key(self, token):
        if self.owner_token and hmac.compare_digest(token, self.owner_token):
            return "owner", True
        if not re.fullmatch(r"sat_[a-f0-9]{64}\.[a-f0-9]{64}", token):
            raise AccessError("unauthorized", 401)
        payload, signature = token.split(".")
        if not hmac.compare_digest(signature, self.signature(payload)):
            raise AccessError("unauthorized", 401)
        return "token_" + digest(token), False

    def finish(self, result, now):
        if isinstance(result, AccessError):
            # Avoid repeated reads after the shared HTTP storage budget is exhausted.
            if result.code in ("http_day_limit", "http_month_limit"):
                self.global_block_until = now + result.retry_after
            raise result
        return result

    def http_budget(self, state, p, now):
        for name, period, limit in (("http_day", p["day"], self.limits.http_daily),
                                    ("http_month", p["month"], self.limits.http_monthly)):
            error = exhausted(state, name, period, limit, now)
            if error:
                return error
        increment(state, "http_day", p["day"])
        increment(state, "http_month", p["month"])
        return None

    def register(self, email):
        if not isinstance(email, str):
            raise AccessError("invalid_email", 400)
        email = email.strip().casefold()
        if len(email) > 254 or not re.fullmatch(r"[a-z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-z0-9-]+(?:\.[a-z0-9-]+)+", email):
            raise AccessError("invalid_email", 400)
        now = self.clock()
        if now < self.global_block_until:
            raise AccessError("service_allowance_limit", retry_after=self.global_block_until - now)
        p, token = periods(now), self.new_token()
        token_id, _ = self.token_key(token)
        email_id = "email_" + hmac.new(self.key, ("email:" + email).encode(), hashlib.sha256).hexdigest()

        def operation(states):
            global_state = states["global"]
            error = self.http_budget(global_state, p, now)
            if error:
                return error
            for name, period, limit in (("signup_day", p["day"], self.limits.signup_daily),
                                        ("signup_month", p["month"], self.limits.signup_monthly)):
                error = exhausted(global_state, name, period, limit, now)
                if error:
                    return error
            # Duplicate attempts consume the signup allowance too; never recover by email.
            increment(global_state, "signup_day", p["day"])
            increment(global_state, "signup_month", p["month"])
            if states[email_id]:
                return AccessError("registration_unavailable_use_existing_token", 409)
            if global_state.get("accounts", 0) >= self.limits.accounts:
                return AccessError("registration_capacity_reached", 503, 86400)
            account_id = secrets.token_hex(16)
            states[token_id] = {"account_id": account_id, "email": email, "email_verified": False,
                                "active": True, "created_at": int(now)}
            states[email_id] = {"account_id": account_id}
            global_state["accounts"] = global_state.get("accounts", 0) + 1
            return {"token": token, "account_id": account_id, "email_verified": False,
                    "daily_tool_limit": self.limits.account_daily}

        return self.finish(self.store.transact(["global", email_id, token_id], operation), now)

    def authorize(self, token, tool=False, revoke=False):
        token_id, owner = self.token_key(token)
        now = self.clock()
        if now < self.global_block_until:
            raise AccessError("service_allowance_limit", retry_after=self.global_block_until - now)
        p = periods(now)

        def operation(states):
            global_state, account = states["global"], states[token_id]
            error = self.http_budget(global_state, p, now)
            if error:
                return error
            if owner and not account:
                account.update(account_id="owner", active=True, created_at=int(now))
            if not account.get("active"):
                return AccessError("unauthorized", 401)
            if revoke:
                if owner:
                    return AccessError("owner_token_managed_by_operator", 403)
                account["active"] = False
                return {"revoked": True}
            if tool:
                checks = [(account, "tools_minute", p["minute"], self.limits.account_minute),
                          (account, "tools_day", p["day"], self.limits.account_daily),
                          (global_state, "tools_day", p["day"], self.limits.global_daily),
                          (global_state, "tools_month", p["month"], self.limits.global_monthly)]
                for state, name, period, limit in checks:
                    error = exhausted(state, name, period, limit, now)
                    if error:
                        error.code = ("account_" if state is account else "service_") + error.code
                        return error
                for state, name, period, _ in checks:
                    increment(state, name, period)
            return {"account_id": account["account_id"], "daily_tool_limit": self.limits.account_daily,
                    "daily_tool_used": count(account, "tools_day", p["day"]),
                    "daily_tool_remaining": self.limits.account_daily - count(account, "tools_day", p["day"]),
                    "resets_at": datetime.fromtimestamp(p["day"][1], UTC).isoformat(),
                    "shared_tool_remaining_today": max(0, self.limits.global_daily -
                                                       count(global_state, "tools_day", p["day"])),
                    "shared_tool_remaining_month": max(0, self.limits.global_monthly -
                                                       count(global_state, "tools_month", p["month"]))}

        return self.finish(self.store.transact(["global", token_id], operation), now)
