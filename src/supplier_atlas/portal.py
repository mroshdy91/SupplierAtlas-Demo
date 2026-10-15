"""Same-origin onboarding and bearer-authenticated account page. No email delivery."""
import asyncio
import json
import time
from collections import deque
from fnmatch import fnmatchcase
from pathlib import Path
from urllib.parse import urlsplit

from starlette.concurrency import run_in_threadpool
from starlette.responses import JSONResponse, Response

from .access import AccessError

WEB = Path(__file__).with_name("web")
SECURITY_HEADERS = {
    "Cache-Control": "no-store",
    "X-Content-Type-Options": "nosniff",
    "Referrer-Policy": "no-referrer",
    "Content-Security-Policy": "default-src 'none'; script-src 'self'; style-src 'self'; "
                               "connect-src 'self'; img-src 'self'; frame-ancestors 'none'; "
                               "base-uri 'none'; form-action 'self'",
}


class PortalGate:
    def __init__(self, app, access, allowed_hosts, clock=time.monotonic):
        self.app, self.access, self.allowed_hosts = app, access, allowed_hosts
        self.clock, self.requests, self.signups = clock, deque(), deque()

    def rate(self, queue, limit):
        now = self.clock()
        while queue and queue[0] <= now - 60:
            queue.popleft()
        if len(queue) >= limit:
            raise AccessError("burst_limit", retry_after=60 - (now - queue[0]))
        queue.append(now)

    async def body(self, receive, limit=65536):
        chunks, size = [], 0
        while True:
            message = await asyncio.wait_for(receive(), timeout=5)
            if message["type"] == "http.disconnect":
                raise AccessError("disconnected", 400)
            chunk = message.get("body", b"")
            size += len(chunk)
            if size > limit:
                raise AccessError("request_too_large", 413)
            chunks.append(chunk)
            if not message.get("more_body"):
                return b"".join(chunks)

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            return await self.app(scope, receive, send)

        async def respond(value, status=200, headers=None):
            await JSONResponse(value, status_code=status,
                               headers={**SECURITY_HEADERS, **(headers or {})})(scope, receive, send)

        try:
            self.rate(self.requests, 120)
            headers = dict(scope["headers"])
            host = headers.get(b"host", b"").decode("latin1").lower()
            if not any(fnmatchcase(host, allowed.lower()) for allowed in self.allowed_hosts):
                raise AccessError("invalid_host", 400)
            origin = headers.get(b"origin")
            if origin:
                parsed = urlsplit(origin.decode("latin1"))
                local = parsed.hostname in ("localhost", "127.0.0.1", "testserver")
                if parsed.netloc.lower() != host or parsed.scheme not in (("http", "https") if local else ("https",)):
                    raise AccessError("origin_not_allowed", 403)
            path, method = scope["path"], scope["method"]
            assets = {"/": ("index.html", "text/html"), "/portal.js": ("portal.js", "text/javascript"),
                      "/portal.css": ("portal.css", "text/css")}
            if path in assets and method in ("GET", "HEAD"):
                name, media = assets[path]
                content = (WEB / name).read_bytes() if method == "GET" else b""
                return await Response(content, media_type=media, headers=SECURITY_HEADERS)(scope, receive, send)
            if path == "/health" and method == "GET":
                return await self.app(scope, receive, send)
            if path == "/api/register" and method == "POST":
                self.rate(self.signups, 5)
                if headers.get(b"content-type", b"").split(b";")[0] != b"application/json":
                    raise AccessError("json_required", 415)
                data = json.loads(await self.body(receive, 1024))
                if not isinstance(data, dict) or set(data) != {"email"}:
                    raise AccessError("email_required", 400)
                result = await run_in_threadpool(self.access.register, data["email"])
                return await respond(result, 201)
            is_mcp = path in ("/mcp", "/mcp/")
            if not is_mcp and (path, method) not in (("/api/account", "GET"), ("/api/revoke", "POST")):
                return await respond({"error": "not_found"}, 404)
            authorization = headers.get(b"authorization", b"").decode("latin1")
            token = authorization[7:] if authorization.startswith("Bearer ") else ""
            self.access.token_key(token)  # Reject invalid signatures without database access.
            tool, raw = False, None
            if is_mcp and method == "POST":
                raw = await self.body(receive)
                data = json.loads(raw)
                if not isinstance(data, dict):
                    raise AccessError("json_rpc_object_required", 400)
                tool = data.get("method") == "tools/call"
            account = await run_in_threadpool(self.access.authorize, token, tool, path == "/api/revoke")
            if not is_mcp:
                return await respond(account)

            async def replay():
                nonlocal raw
                if raw is not None:
                    body, raw = raw, None
                    return {"type": "http.request", "body": body, "more_body": False}
                return await receive()

            async def secure_send(message):
                if message["type"] == "http.response.start":
                    message["headers"] = list(message.get("headers", [])) + [
                        (b"cache-control", b"no-store"),
                        (b"x-ratelimit-remaining", str(account["daily_tool_remaining"]).encode()),
                        (b"x-ratelimit-reset", account["resets_at"].encode())]
                await send(message)

            return await self.app(scope, replay, secure_send)
        except AccessError as error:
            extra = {"Retry-After": str(error.retry_after)} if error.status in (429, 503) else {}
            if error.status == 401:
                extra["WWW-Authenticate"] = "Bearer"
            return await respond({"error": error.code}, error.status, extra)
        except (ValueError, UnicodeError):
            return await respond({"error": "invalid_request"}, 400)
        except TimeoutError:
            return await respond({"error": "request_timeout"}, 408)
        except Exception:  # noqa: BLE001 -- public boundary must fail closed without leaking SDK payloads
            # Fail closed, without logging secrets, emails, requests or SDK exception payloads.
            return await respond({"error": "access_service_unavailable"}, 503, {"Retry-After": "60"})
