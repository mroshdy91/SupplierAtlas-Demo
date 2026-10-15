import asyncio
import json
import sys
from pathlib import Path

from mcp import Client, StdioServerParameters
from starlette.testclient import TestClient

from supplier_atlas.query import Catalog
from supplier_atlas.server import create_app, create_server

ROOT = Path(__file__).parents[1]


def test_three_tools_protocol_and_structured_output():
    async def scenario():
        async with Client(create_server(Catalog(ROOT / "data/catalog.sqlite"))) as client:
            tools = await client.list_tools()
            assert {t.name for t in tools.tools} == {"discover_catalog", "search_products", "get_products"}
            result = await client.call_tool("discover_catalog", {"request": {}})
            assert not result.is_error
            assert next(c for c in result.structured_content["categories"]
                        if c["id"] == "air_outlets.ceiling_diffusers")["models"] == 2
            assert json.loads(result.content[0].text) == result.structured_content
            error = await client.call_tool("search_products", {"request": {"category": "missing"}})
            assert error.is_error
    asyncio.run(scenario())


def test_stdio_real_process():
    async def scenario():
        async with Client(StdioServerParameters(command=sys.executable, args=["-m", "supplier_atlas.server",
                "--catalog", str(ROOT / "data/catalog.sqlite")])) as client:
            result = await client.call_tool("get_products", {"request": {"ids": ["alsharqa.scd.6x6"],
                "tables": [{"table_id": "alsharqa.scd.supply", "columns": ["nc"], "limit": 1}]}})
            assert not result.is_error
            assert result.structured_content["products"][0]["data"][0]["rows"][0]["values"] == [63, {"value": 18, "qualifier": "lt"}]
    asyncio.run(scenario())


def test_http_auth_and_health():
    app = create_app(Catalog(ROOT / "data/catalog.sqlite"), token="test-token")
    with TestClient(app) as client:
        assert client.get("/health").json()["status"] == "ok"
        assert client.post("/mcp", json={}).status_code == 401
        assert client.post("/mcp", headers={"Authorization": "Bearer wrong"}, json={}).status_code == 401
        response = client.post("/mcp", headers={"Authorization": "Bearer test-token", "Accept": "application/json, text/event-stream"},
            json={"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {"protocolVersion": "2025-06-18",
                  "capabilities": {}, "clientInfo": {"name": "test", "version": "1"}}})
        assert response.status_code == 200
        assert response.json()["result"]["serverInfo"]["name"] == "SupplierAtlas"
