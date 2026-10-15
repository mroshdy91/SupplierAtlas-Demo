"""Verify personal-token onboarding against HTTP; never print the issued token."""
import argparse
import asyncio
import secrets

import httpx2
from mcp.client.streamable_http import streamable_http_client
from smoke_http import check


async def main(base):
    base = base.rstrip("/")
    async with httpx2.AsyncClient(timeout=30) as http:
        page = await http.get(base + "/")
        assert page.status_code == 200 and "No verification email" in page.text
        assert "frame-ancestors 'none'" in page.headers["Content-Security-Policy"]
        for path in ("/portal.js", "/portal.css"):
            assert (await http.get(base + path)).status_code == 200
        assert (await http.get(base + "/api/account")).status_code == 401
        email = "smoke-" + secrets.token_hex(5) + "@example.invalid"
        registration = await http.post(base + "/api/register", json={"email": email})
        assert registration.status_code == 201, (registration.status_code, registration.text)
        token = registration.json()["token"]
        assert registration.headers["Cache-Control"] == "no-store"
        headers = {"Authorization": "Bearer " + token}
        try:
            before = (await http.get(base + "/api/account", headers=headers)).json()
            assert before["daily_tool_used"] == 0
            async with httpx2.AsyncClient(headers=headers, timeout=30) as authenticated:
                await check(streamable_http_client(base + "/mcp", http_client=authenticated))
            after = (await http.get(base + "/api/account", headers=headers)).json()
            assert after["daily_tool_used"] == 6
            assert after["daily_tool_remaining"] == before["daily_tool_remaining"] - 6
            duplicate = await http.post(base + "/api/register", json={"email": email})
            assert duplicate.status_code == 409 and token not in duplicate.text
            invalid = await http.get(base + "/api/account", headers={"Authorization": "Bearer " + token + "0"})
            assert invalid.status_code == 401
            print("Personal access: page/assets, signup, 6 engineering calls, exact usage, duplicate protection and invalid token passed.")
        finally:
            revoked = await http.post(base + "/api/revoke", headers=headers)
            assert revoked.status_code == 200
            assert (await http.get(base + "/api/account", headers=headers)).status_code == 401
            print("Test personal token revoked and rejection verified.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("base")
    asyncio.run(main(parser.parse_args().base))
