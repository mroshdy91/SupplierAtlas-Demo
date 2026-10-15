# SupplierAtlas demo

Structured engineering product data for AI agents through three read-only MCP
tools: `discover_catalog`, `search_products`, and `get_products`.

[Current deployment provenance](docs/DEPLOYMENT.md) and
[five-reviewer data-quality audit](docs/DATA_QUALITY_AUDIT.md).

The reviewed dataset spans all 22 Alsharqa catalogs: 37 models, 76 tables and
3,707 engineering rows. It is a data service, not a suitability or supplier-rating
engine. Units, conditions, bounds
and page references are retained; advertising and company history are excluded.

Official index: [Alsharqa products](https://alsharqa.com/products/).
See [coverage](docs/ALSHARQA_COVERAGE.md), [source issues](docs/SOURCE_ISSUES.md),
and `datasets/alsharqa/source_inventory.json` for URLs, page dispositions and hashes.
The unlabeled VCD matrix and obscured cells remain withheld; graphs are not digitized.
Printed document dates are unknown. Original PDFs are not distributed here.
Manufacturer data remains attributed to
its source; no independent performance certification is claimed.

Five fresh-context Sol reviews compared 1,798 sampled row/column values against
rendered PDFs across all 76 tables and stressed retrieval semantics. One import
error and two context omissions were corrected. All 43 tests pass, including the
new source-sample fixture. Untested cells may still contain errors; see the audit
for exact coverage, supplier inconsistencies and remaining limits.

The public container includes backend code and this reviewed dataset. It does
not contain deployment credentials. CI validates the structured package and runs
protocol and container tests before publishing revision-specific image tags to
`ghcr.io/mroshdy91/supplieratlas-demo`. CI rebuilds the reviewed transcription;
it does not download or independently re-check the original PDFs. Generated
`catalog.json` and SQLite snapshots are build outputs, not committed input files.

## Local use

Install `requirements.txt`, then install this project with `pip install --no-deps .`.
Run `python datasets/alsharqa/prepare.py`, followed by
`supplier-atlas-build datasets/alsharqa/catalog.json data/catalog.sqlite`.
Run `supplier-atlas` for stdio, or `supplier-atlas --transport http` for localhost HTTP.

Remote HTTP requires a token and cursor key of at least 32 characters in
`SUPPLIER_ATLAS_TOKEN` and `SUPPLIER_ATLAS_CURSOR_KEY`, plus the explicit hostname
allowlist `SUPPLIER_ATLAS_ALLOWED_HOSTS`. `/mcp` provides the MCP endpoint;
`/health` reports service and catalog versions. Never bake secrets into an image.

The operator can deploy an immutable public GHCR digest using
`deploy/deploy.ps1 -Image ghcr.io/mroshdy91/supplieratlas-demo@sha256:...`.
It uses the existing local Google CLI authorization and private runtime environment
file, and keeps service/revision instance maxima at one. No manual file upload is required.
