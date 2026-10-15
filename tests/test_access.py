import json
from concurrent.futures import ThreadPoolExecutor
from datetime import UTC, datetime
from pathlib import Path

import pytest
from starlette.testclient import TestClient

from supplier_atlas.access import AccessError, AccessService, Limits, SQLiteAccessStore, periods
from supplier_atlas.query import Catalog
from supplier_atlas.server import create_app

ROOT = Path(__file__).parents[1]
KEY = "test-signing-key-" * 4


def service(tmp_path, **limits):
    return AccessService(SQLiteAccessStore(tmp_path / "access.sqlite"), KEY, "owner-test-token",
                         Limits(**limits), clock=lambda: 1792065600)


def register(access, email="engineer@example.invalid"):
    return access.register(email)["token"]


def test_unverified_registration_hash_only_and_no_email_recovery(tmp_path):
    access = service(tmp_path)
    result = access.register(" Engineer@Example.invalid ")
    token = result["token"]
    assert result["email_verified"] is False
    assert access.authorize(token)["daily_tool_remaining"] == 100
    assert token.encode() not in (tmp_path / "access.sqlite").read_bytes()
    with pytest.raises(AccessError) as error:
        access.register("engineer@example.invalid")
    assert error.value.status == 409
    assert access.authorize(token)["account_id"] == result["account_id"]


@pytest.mark.parametrize("email", [None, "x", "a@b", "a\n@example.com", "x" * 250 + "@example.com"])
def test_invalid_email(tmp_path, email):
    with pytest.raises(AccessError) as error:
        service(tmp_path).register(email)
    assert error.value.status == 400


def test_forged_token_does_not_touch_storage(tmp_path):
    access = service(tmp_path)
    token = access.new_token()
    access.store = None
    for invalid in ("", "garbage", token[:-1] + ("0" if token[-1] != "0" else "1")):
        with pytest.raises(AccessError) as error:
            access.authorize(invalid)
        assert error.value.status == 401


def test_account_daily_limit_persistence_and_utc_reset(tmp_path):
    access = service(tmp_path, account_daily=2)
    token = register(access)
    access.authorize(token, tool=True)
    restarted = service(tmp_path, account_daily=2)
    assert restarted.authorize(token, tool=True)["daily_tool_remaining"] == 0
    with pytest.raises(AccessError) as error:
        restarted.authorize(token, tool=True)
    assert error.value.code == "account_tools_day_limit"
    assert restarted.authorize(token)["daily_tool_used"] == 2  # status/initialization aren't tool calls
    restarted.clock = lambda: 1792065600 + 86400
    assert restarted.authorize(token, tool=True)["daily_tool_remaining"] == 1


def test_shared_limits_include_owner_and_all_accounts(tmp_path):
    access = service(tmp_path, global_daily=2)
    token = register(access)
    access.authorize("owner-test-token", tool=True)
    access.authorize(token, tool=True)
    with pytest.raises(AccessError) as error:
        access.authorize("owner-test-token", tool=True)
    assert error.value.code == "service_tools_day_limit"


def test_month_limit_survives_daily_reset(tmp_path):
    access = service(tmp_path, global_monthly=1)
    token = register(access)
    access.authorize(token, tool=True)
    access.clock = lambda: 1792065600 + 86400
    with pytest.raises(AccessError) as error:
        access.authorize(token, tool=True)
    assert error.value.code == "service_tools_month_limit"
    access.clock = lambda: datetime(2026, 11, 1, tzinfo=UTC).timestamp()
    assert access.authorize(token, tool=True)["daily_tool_remaining"] == 99


def test_minute_and_calendar_boundaries(tmp_path):
    access = service(tmp_path, account_minute=1)
    token = register(access)
    access.authorize(token, tool=True)
    with pytest.raises(AccessError) as error:
        access.authorize(token, tool=True)
    assert error.value.code == "account_tools_minute_limit"
    access.clock = lambda: 1792065660
    assert access.authorize(token, tool=True)["daily_tool_used"] == 2
    date = datetime(2026, 12, 31, 23, 59, 59, tzinfo=UTC).timestamp()
    assert periods(date)["month"][1] == datetime(2027, 1, 1, tzinfo=UTC).timestamp()


def test_concurrent_instances_cannot_overspend(tmp_path):
    first = service(tmp_path, account_daily=5)
    second = service(tmp_path, account_daily=5)
    token = register(first)

    def attempt(index):
        try:
            (first if index % 2 else second).authorize(token, tool=True)
            return True
        except AccessError:
            return False

    with ThreadPoolExecutor(max_workers=8) as pool:
        assert sum(pool.map(attempt, range(20))) == 5
    assert second.authorize(token)["daily_tool_used"] == 5


def test_global_http_cap_and_cache_fail_closed(tmp_path):
    access = service(tmp_path, http_daily=2)
    token = register(access)
    access.authorize(token)
    with pytest.raises(AccessError) as error:
        access.authorize(token)
    assert error.value.code == "http_day_limit"
    access.store = None  # Further requests hit cached rejection, not storage.
    with pytest.raises(AccessError) as error:
        access.authorize(token)
    assert error.value.code == "service_allowance_limit"


def test_duplicate_signup_consumes_allowance_and_capacity(tmp_path):
    access = service(tmp_path, signup_daily=2)
    register(access)
    with pytest.raises(AccessError):
        register(access)
    with pytest.raises(AccessError) as error:
        register(access, "another@example.invalid")
    assert error.value.code == "signup_day_limit"
    limited = service(tmp_path, accounts=1)
    with pytest.raises(AccessError) as error:
        register(limited, "third@example.invalid")
    assert error.value.code == "registration_capacity_reached"


def test_revocation_survives_restart(tmp_path):
    access = service(tmp_path)
    token = register(access)
    assert access.authorize(token, revoke=True) == {"revoked": True}
    with pytest.raises(AccessError) as error:
        service(tmp_path).authorize(token)
    assert error.value.status == 401
    with pytest.raises(AccessError):
        register(access)  # Email never resets a revoked account's credential.


def test_portal_authorization_protocol_account_and_errors(tmp_path):
    access = service(tmp_path, account_daily=1)
    app = create_app(Catalog(ROOT / "data/catalog.sqlite"), access=access)
    with TestClient(app) as client:
        page = client.get("/")
        assert page.status_code == 200 and "No verification email" in page.text
        assert "frame-ancestors 'none'" in page.headers["Content-Security-Policy"]
        assert client.get("/portal.js").status_code == 200
        assert client.get("/portal.css").status_code == 200
        assert client.get("/api/account").status_code == 401
        assert client.post("/api/register", json={"email": "x@example.invalid"},
                           headers={"Origin": "https://attacker.invalid"}).status_code == 403
        registered = client.post("/api/register", json={"email": "x@example.invalid"})
        assert registered.status_code == 201 and registered.headers["Cache-Control"] == "no-store"
        token = registered.json()["token"]
        headers = {"Authorization": "Bearer " + token, "Accept": "application/json, text/event-stream"}
        init = client.post("/mcp", headers=headers, json={"jsonrpc": "2.0", "id": 1, "method": "initialize",
            "params": {"protocolVersion": "2025-06-18", "capabilities": {},
                       "clientInfo": {"name": "test", "version": "1"}}})
        assert init.status_code == 200
        assert client.get("/api/account", headers=headers).json()["daily_tool_used"] == 0
        body = {"jsonrpc": "2.0", "id": 2, "method": "tools/call",
                "params": {"name": "discover_catalog", "arguments": {"request": {}}}}
        response = client.post("/mcp", headers=headers, json=body)
        assert response.status_code == 200 and "categories" in response.json()["result"]["structuredContent"]
        assert response.headers["x-ratelimit-remaining"] == "0"
        limited = client.post("/mcp", headers=headers, json=body)
        assert limited.status_code == 429 and int(limited.headers["Retry-After"]) > 0
        assert client.get("/api/account", headers=headers).json()["daily_tool_used"] == 1
        assert client.post("/mcp", headers=headers, content="[{}]").status_code == 400
        assert client.post("/mcp", headers=headers, content="x" * 65537).status_code == 413
        assert client.get("/", headers={"Host": "attacker.invalid"}).status_code == 400
        assert client.post("/api/revoke", headers=headers).json() == {"revoked": True}
        assert client.get("/api/account", headers=headers).status_code == 401
        # Neither raw token nor email is echoed in authorized status/errors.
        assert token not in limited.text and "x@example.invalid" not in limited.text


def test_storage_failure_never_allows_request(tmp_path):
    access = service(tmp_path)
    token = register(access)
    access.store = None
    app = create_app(Catalog(ROOT / "data/catalog.sqlite"), access=access)
    with TestClient(app) as client:
        result = client.get("/api/account", headers={"Authorization": "Bearer " + token})
        assert result.status_code == 503
        assert result.json() == {"error": "access_service_unavailable"}


def test_public_burst_limit_and_signup_limit(tmp_path):
    app = create_app(Catalog(ROOT / "data/catalog.sqlite"), access=service(tmp_path))
    with TestClient(app) as client:
        for i in range(5):
            assert client.post("/api/register", json={"email": f"x{i}@example.invalid"}).status_code == 201
        assert client.post("/api/register", json={"email": "x6@example.invalid"}).status_code == 429
        for _ in range(114):
            client.get("/missing")
        assert client.get("/").status_code == 429


def test_store_does_not_persist_unbounded_history(tmp_path):
    access = service(tmp_path)
    token = register(access)
    access.authorize(token, tool=True)
    key, _ = access.token_key(token)
    state = access.store.transact([key], lambda states: states[key])
    assert set(state) == {"account_id", "email", "email_verified", "active", "created_at", "tools_minute", "tools_day"}
    assert "token" not in json.dumps(state)
