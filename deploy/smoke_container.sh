#!/usr/bin/env bash
# Container verification in free Cloud Shell; does not deploy a paid resource.
set -euo pipefail
umask 077
smoke_env=$(mktemp)
container=""
cleanup() {
  result=$?
  if [ "$result" -ne 0 ] && [ -n "$container" ]; then docker logs --tail=40 "$container" >&2; fi
  if [ -n "$container" ]; then docker rm -f "$container" >/dev/null; fi
  rm -f "$smoke_env"
}
trap cleanup EXIT
python3 - "$smoke_env" <<'PY'
import secrets
import sys
from pathlib import Path
Path(sys.argv[1]).write_text(
    'PORT=8080\nSUPPLIER_ATLAS_ALLOWED_HOSTS=127.0.0.1:*\n'
    'SUPPLIER_ATLAS_TOKEN=' + secrets.token_urlsafe(48) + '\n'
    'SUPPLIER_ATLAS_CURSOR_KEY=' + secrets.token_urlsafe(48) + '\n')
PY
container=$(docker run -d --env-file "$smoke_env" --memory=256m --cpus=0.5 supplieratlas-demo:local)
docker cp scripts/smoke_http.py "$container:/tmp/smoke_http.py"
# Bounded readiness polling, performed inside the isolated container.
docker exec -i "$container" python - <<'PY'
import json
import time
import urllib.error
import urllib.request
for attempt in range(30):
    try:
        with urllib.request.urlopen('http://127.0.0.1:8080/health', timeout=2) as response:
            health = json.load(response)
        assert health['status'] == 'ok'
        print('Container health:', health)
        break
    except (OSError, urllib.error.URLError):
        time.sleep(1)
else:
    raise RuntimeError('Container did not become ready')
try:
    urllib.request.urlopen('http://127.0.0.1:8080/mcp')
except urllib.error.HTTPError as exc:
    assert exc.code == 401, exc.code
    print('Unauthorized MCP request correctly rejected (401).')
else:
    raise AssertionError('Unauthenticated MCP request unexpectedly succeeded')
PY
docker exec "$container" python /tmp/smoke_http.py http://127.0.0.1:8080/mcp
docker image inspect supplieratlas-demo:local --format='Container image size: {{.Size}} bytes'
