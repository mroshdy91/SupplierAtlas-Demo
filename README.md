# SupplierAtlas demo

Structured engineering product data for AI agents through three read-only MCP
tools: `discover_catalog`, `search_products`, and `get_products`.

The reviewed demo covers Alsharqa SCD nominal 6x6, 9x9 and 12x12 inch neck sizes:
21 four-way supply operating points and 21 return points. It is partial catalog
coverage, not a suitability or supplier-rating engine. Units, conditions, bounds
and page references are retained; advertising and company history are excluded.

Official source: [Alsharqa ceiling diffusers](https://alsharqa.com/wp-content/uploads/2025/04/ceiling-diffusers.pdf),
printed pages 7, 9, 19 and 20. Printed document date is unknown. Reviewed PDF SHA-256:
`6548714c85b082cda1206210774a42baea2fd164b7e1a39058a977e9c50e57df`.
The PDF itself is not distributed here. Manufacturer data remains attributed to
its source; no independent performance certification is claimed.

The public container includes backend code and this reviewed dataset. It does
not contain deployment credentials. CI validates the structured package and runs
protocol and container tests before publishing revision-specific image tags to
`ghcr.io/mroshdy91/supplieratlas-demo`. CI rebuilds the reviewed transcription;
it does not download or independently re-check the original PDF.

## Local use

Install `requirements.txt`, then install this project with `pip install --no-deps .`.
Run `python datasets/alsharqa/prepare.py`, followed by
`supplier-atlas-build datasets/alsharqa/catalog.json data/catalog.sqlite`.
Run `supplier-atlas` for stdio, or `supplier-atlas --transport http` for localhost HTTP.

Remote HTTP requires a token and cursor key of at least 32 characters in
`SUPPLIER_ATLAS_TOKEN` and `SUPPLIER_ATLAS_CURSOR_KEY`, plus the explicit hostname
allowlist `SUPPLIER_ATLAS_ALLOWED_HOSTS`. `/mcp` provides the MCP endpoint;
`/health` reports service and catalog versions. Never bake secrets into an image.

