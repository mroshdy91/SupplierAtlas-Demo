#!/usr/bin/env bash
# Run from a deployment bundle transferred by deploy/cloudshell.ps1.
# Billing linkage and project choice are intentionally explicit prerequisites.
set -euo pipefail
echo 'Legacy bootstrap retired: use deploy/deploy.ps1 with an immutable GHCR digest and durable access storage.' >&2
exit 2
project="supplieratlas-demo-20261015"
region="us-central1"
service="supplieratlas-demo"
# The shared billing account exceeded its registry free allowance on 2026-10-15.
# Never push a new image merely because a new project was created.
if [ -z "${SUPPLIER_ATLAS_IMAGE:-}" ]; then
  echo 'Deployment held: supply an approved existing image URL after the registry cost review.' >&2
  exit 2
fi
gcloud config set project "$project" >/dev/null
test "$(gcloud billing projects describe "$project" --format='value(billingEnabled)')" = "True"
gcloud services enable run.googleapis.com --project "$project"
image="$SUPPLIER_ATLAS_IMAGE"
# Persist secrets only in a private Cloud Shell file, never logs or source bundles.
umask 077
if [ ! -f .runtime.env.yaml ]; then
  python3 - <<'PY'
import secrets
from pathlib import Path
Path('.runtime.env.yaml').write_text(
    'SUPPLIER_ATLAS_TOKEN: "' + secrets.token_urlsafe(48) + '"\n'
    'SUPPLIER_ATLAS_CURSOR_KEY: "' + secrets.token_urlsafe(48) + '"\n'
    'SUPPLIER_ATLAS_ALLOWED_HOSTS: "supplieratlas-demo-524685338738.us-central1.run.app"\n')
PY
fi
# Initially IAM-private. Opening invocation for token-authenticated MCP clients
# is a separate explicit step after deployment verification and access review.
gcloud run deploy "$service" --project="$project" --region="$region" --image="$image" \
  --no-allow-unauthenticated --min=0 --max=1 --cpu=0.5 --memory=256Mi \
  --concurrency=1 --timeout=30 --execution-environment=gen1 --no-cpu-boost \
  --cpu-throttling --env-vars-file=.runtime.env.yaml --quiet
gcloud run services describe "$service" --project="$project" --region="$region" \
  --format='yaml(status.url,status.conditions,spec.template.metadata.annotations,spec.template.spec.containers[0].resources)'
