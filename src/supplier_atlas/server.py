"""Exactly three read-only tools, available over stdio or Streamable HTTP."""
import argparse
import hmac
import os
import time
from collections import deque

import uvicorn
from mcp.server import MCPServer
from mcp.server.transport_security import TransportSecuritySettings
from mcp.types import CallToolResult, TextContent, ToolAnnotations
from starlette.responses import JSONResponse
from starlette.routing import Route

from . import __version__
from .ingestion import encoded
from .models import DiscoverRequest, GetRequest, SearchRequest
from .query import Catalog, QueryError


def create_server(catalog):
    server = MCPServer("SupplierAtlas", version=__version__, instructions=(
        "Retrieve published engineering product data. Discover vocabulary, search unknown products, "
        "get requested data for known IDs. Observe coverage, units, bounds and operating conditions. "
        "This service does not calculate or decide engineering suitability."))
    annotations = ToolAnnotations(read_only_hint=True, open_world_hint=False)

    def run(function, request):
        try:
            value = function(request)
            # Compact JSON text is the compatibility representation required by older clients.
            return CallToolResult(content=[TextContent(type="text", text=encoded(value))], structured_content=value)
        except QueryError as exc:
            return CallToolResult(content=[TextContent(type="text", text=str(exc))], is_error=True)

    @server.tool(annotations=annotations)
    def discover_catalog(request: DiscoverRequest) -> CallToolResult:
        """Discover category coverage and property/schema IDs. Use schema_id for columns and units; no products returned."""
        return run(catalog.discover, request)

    @server.tool(annotations=annotations)
    def search_products(request: SearchRequest) -> CallToolResult:
        """Find unknown product IDs by name/properties or one table's same-row conditions. Returns one matching example per model, no suitability ranking."""
        return run(catalog.search, request)

    @server.tool(annotations=annotations)
    def get_products(request: GetRequest) -> CallToolResult:
        """Retrieve known IDs in batches up to 5. Default gives overview and table descriptors; request table IDs/columns/filters for bounded rows."""
        return run(catalog.get, request)

    return server


class AccessGate:
    """Single demo credential; per-instance request limit. Never logs credentials."""
    def __init__(self, app, token=None, limit=120):
        self.app, self.token, self.limit = app, token, limit
        self.requests = deque()

    async def __call__(self, scope, receive, send):
        if scope["type"] == "http" and scope["path"] != "/health":
            headers = dict(scope["headers"])
            provided = headers.get(b"authorization", b"").decode("latin1")
            if self.token and not hmac.compare_digest(provided, "Bearer " + self.token):
                await JSONResponse({"error": "Unauthorized"}, status_code=401)(scope, receive, send)
                return
            now = time.monotonic()
            while self.requests and self.requests[0] < now - 60:
                self.requests.popleft()
            if len(self.requests) >= self.limit:
                await JSONResponse({"error": "Rate limit"}, status_code=429,
                                   headers={"Retry-After": "60"})(scope, receive, send)
                return
            self.requests.append(now)
        await self.app(scope, receive, send)


def create_app(catalog, token=None, allowed_hosts=None, access=None):
    server = create_server(catalog)
    app = server.streamable_http_app(stateless_http=True, json_response=True, max_request_body_size=65536,
        transport_security=TransportSecuritySettings(allowed_hosts=allowed_hosts or ["127.0.0.1:*", "localhost:*", "testserver"],
                                                     allowed_origins=[]))

    async def health(request):
        with catalog.connect() as db:
            version, _ = catalog.release(db)
        return JSONResponse({"status": "ok", "service_version": __version__, "catalog_version": version})

    app.routes.append(Route("/health", health))
    if access:
        from .portal import PortalGate
        return PortalGate(app, access, allowed_hosts or ["127.0.0.1:*", "localhost:*", "testserver"])
    return AccessGate(app, token)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--catalog", default=os.environ.get("SUPPLIER_ATLAS_DB", "data/catalog.sqlite"))
    parser.add_argument("--transport", choices=["stdio", "http"], default="stdio")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=int(os.environ.get("PORT", "8766")))
    args = parser.parse_args()
    token, key = os.environ.get("SUPPLIER_ATLAS_TOKEN"), os.environ.get("SUPPLIER_ATLAS_CURSOR_KEY")
    hosts = os.environ.get("SUPPLIER_ATLAS_ALLOWED_HOSTS")
    if (args.transport == "http" and args.host not in ("127.0.0.1", "localhost", "::1")
            and (not token or len(token) < 32 or not key or len(key) < 32 or not hosts)):
        parser.error("Remote HTTP requires token and cursor key (32+ chars), and explicit allowed hosts")
    catalog = Catalog(args.catalog, key)
    if args.transport == "stdio":
        create_server(catalog).run()
    else:
        access = None
        backend = os.environ.get("SUPPLIER_ATLAS_ACCESS_BACKEND")
        if backend:
            from .access import AccessService, FirestoreAccessStore, Limits, SQLiteAccessStore
            if backend == "firestore":
                store = FirestoreAccessStore(os.environ["SUPPLIER_ATLAS_ACCESS_PROJECT"])
            elif backend == "sqlite" and not os.environ.get("K_SERVICE"):
                store = SQLiteAccessStore(os.environ.get("SUPPLIER_ATLAS_ACCESS_DB", "data/access.sqlite"))
            else:
                parser.error("Access backend must be firestore (hosted) or sqlite (local development only)")
            access = AccessService(store, key, token, Limits.from_env())
        if os.environ.get("K_SERVICE") and not access:
            parser.error("Hosted service requires durable access storage")
        uvicorn.run(create_app(catalog, token, hosts.split(",") if hosts else None, access), host=args.host, port=args.port,
                    access_log=False)


if __name__ == "__main__":
    main()
