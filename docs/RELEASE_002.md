# Alsharqa engineering release 002

Verified 2026-10-15. All 22 published Alsharqa catalogs reviewed: 37 model records,
76 technical tables, 3,707 rows. See [coverage](ALSHARQA_COVERAGE.md) and
[source qualifications](SOURCE_ISSUES.md). Original 42 SCD row IDs remain stable.

- Catalog: `alsharqa-engineering-002+935114259de3`.
- Runtime commit: `8a4b45e5ade2ca1a165c36bb6db9c9b48fa93ae5`.
- [CI evidence](https://github.com/mroshdy91/SupplierAtlas-Demo/actions/runs/38743151751): 32 tests and container HTTP checks passed.
- Image: `ghcr.io/mroshdy91/supplieratlas-demo@sha256:4623b5a0485459b5ed2e1673c5213c33355b914dc293ded8ee47914a9c60b9c1`.
- Cloud Run revision: `supplieratlas-demo-00003-crh`, 100% traffic.
- [Hosted health](https://supplieratlas-demo-524685338738.us-central1.run.app/health) reports the expected catalog. Unauthenticated MCP requests return 401.

Hosted SDK and installed SupplierAtlas plugin calls passed discovery, search and
retrieval. Expanded ceiling, Flow Bar, damper and duct hardware rows were checked.
The three-tool contract and existing marketplace plugin remain compatible; a
plugin reinstall is unnecessary.

Explicit row requests omit unrelated variant/table summaries and deduplicate
expanded source locators. Projection preserves table coordinates, units and notes.
For a 20-row ceiling sample, NC-only output measured 2,015 cl100k text tokens
versus 3,129 for all columns. These are deterministic payload measurements,
not independent agent evaluation or guarantees about client context usage.

Deployment remains request-billed and scales to zero: service/revision maxima 1,
0.5 CPU, 256 MiB, concurrency 1, timeout 30 seconds, CPU throttling on, boost off.
The existing gross-usage spend control was not raised. Builds/images use public
GitHub Actions/GHCR; no Google registry or build resource was added. These controls
target free-tier usage but do not guarantee zero charges.

Original PDFs and OCR drafts remain private verification material. CI rebuilds
reviewed matrices; it does not independently inspect the original PDF pages.
