"""Exercise all three tools against a running HTTP endpoint without printing secrets."""
import argparse
import asyncio
import os

import httpx2
from mcp import Client
from mcp.client.streamable_http import streamable_http_client


async def main(url):
    token = os.environ.get("SUPPLIER_ATLAS_TOKEN")
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    identity_token = os.environ.get("SUPPLIER_ATLAS_GOOGLE_ID_TOKEN")
    if identity_token:
        headers["X-Serverless-Authorization"] = f"Bearer {identity_token}"
    async with httpx2.AsyncClient(headers=headers) as http:
        await check(streamable_http_client(url, http_client=http))


async def check(transport):
    async with Client(transport) as client:
        tools = await client.list_tools()
        assert {t.name for t in tools.tools} == {"discover_catalog", "search_products", "get_products"}
        discovery = await client.call_tool("discover_catalog", {"request": {}})
        assert not discovery.is_error
        search = await client.call_tool("search_products", {"request": {"category": "air_outlets.ceiling_diffusers",
            "table": {"schema_id": "ceiling_diffuser.supply.v1", "filters": [{"field": "airflow", "value": 100}]}}})
        assert search.structured_content["products"][0]["matching_variant"] == "alsharqa.scd.6x6"
        detail = await client.call_tool("get_products", {"request": {"ids": ["alsharqa.scd.6x6"], "tables": [
            {"table_id": "alsharqa.scd.supply", "filters": [{"field": "airflow", "value": 100}]}]}})
        assert detail.structured_content["products"][0]["data"][0]["rows"][0]["values"] == [100, .046, 19, 25, 6, 11]
        print("HTTP MCP: initialization, exact three tools, discovery, same-row search and reference retrieval passed.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("url")
    asyncio.run(main(parser.parse_args().url))

