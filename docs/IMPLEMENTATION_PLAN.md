# SupplierAtlas implementation plan

Updated: 2026-10-15. Status: hosted demo live; published marketplace plugin installed and authenticated.

## Implemented progress

- Five user-requested Sol audits completed against original PDFs and installed
  plugin. Corrected one source transcription and two engineering-context omissions.
  Added independently read 1,798-field regression fixture; 43 tests/lint pass.
  See DATA_QUALITY_AUDIT.md for scoped evidence and remaining untested cells.
  Release 004 is live and verified through hosted SDK and seven native calls.
  Plugin guidance alpha.2 is published and marketplace pinned; existing alpha.1
  works with the new backend, with old skill text until the client updates.
- Guided installed-plugin selection trial completed: seven scoped engineering
  scenarios and 32 native calls. Projection context and empty-result diagnostics
  improved; local replay, regression and token results in SELECTION_EVALUATION.md.
  Independent agent and other-client qualification remain future work.
- Additive `context_columns` metadata preserves conditions without new tools or
  changed request schemas. Release 003 has unchanged 37 models /76 tables /3,707 rows.
  Hosted SDK checks and 11 native post-deployment calls match validated local
  responses; exactly three tools remain exposed. See DEPLOYMENT.md.
- User expanded scope to all published Alsharqa product families. Reviewed all
  22 catalogs / 248 pages: 37 models, 76 tables, 3,707 rows packaged and deployed.
  Original 42 reference rows preserved. All 22 source fingerprints verified.
  See ALSHARQA_COVERAGE.md for imports, duplicate pages and explicit exclusions.
- Generic importer, read-only SQLite snapshot, bounded query layer and all three
  MCP tools implemented with official Python SDK 2.3. Locked dependencies in uv.lock.
- 43 tests pass, including cross-family source regressions, 763-row pagination,
  units, source qualification, bounded output, sparse/5,000-row data, stdio and HTTP.
  CI container checks, hosted HTTP and installed native plugin calls also passed.
  Live release: `alsharqa-engineering-004+d28b77646175`; see DEPLOYMENT.md.
- Compact-response measurement and plugin skill validation completed. Codex
  0.162.0-alpha.17.2 on Windows installed the marketplace release and verified
  bearer authentication and exactly three tools. Independent LLM task evaluation
  and live qualification of other clients remain pending.
- Google project `supplieratlas-demo-20261015` created at the user's request.
  Hosted health, unauthenticated rejection, three tool calls and reference data
  passed. Plugin v0.1.0-alpha.1 is published in Atlas Marketplace.
- Verified automated CLI transfer and container build/test in Cloud Shell with
  0.5 CPU / 256 MiB limits. Manual file uploads are no longer required.
- User approved public GHCR publication. GitHub Actions now builds, checks and
  publishes the allowlisted demo backend; local deploy/deploy.ps1 deploys its
  immutable digest. No Google registry or paid build was created. A verified
  USD 0.10 monthly gross-usage Cloud Run spend cap complements scale-to-zero and
  one-instance limits; it does not guarantee zero charges. See DEPLOYMENT.md.

## Outcome

A plugin installed through Atlas Marketplace exposes one supplier's reviewed
engineering data through exactly three generic, read-only MCP tools. Connected
agents use these facts for engineering work. Adding another supplier or category
must not require another public tool.

## Architecture

```text
Official supplier datasheets (found online or supplied by the user)
  -> extraction drafts -> reviewed structured records -> validation
  -> immutable catalog build -> hosted read-only query service
  -> remote MCP -> SupplierAtlas plugin -> connected agent
```

Publication and import are private development operations. Consumer MCP tools do
not modify records. Calculations, interpolation, selection verdicts, supplier
scoring, billing, and automated web collection are outside this demo.

Proposed defaults, not user-mandated technologies:

- Python with typed validation and the official MCP SDK.
- Relational SQLite catalog snapshots for the demo; private original-document
  storage. Read-only snapshots deployed with a container are reproducible and do
  not depend on persistent writes to an ephemeral cloud filesystem.
- Google Cloud Run and Streamable HTTP at `/mcp`; authenticate using credentials
  supported by the first tested client. Do not assume all clients share the same
  auth flow. Credentials never enter public manifests or catalog snapshots.
- Public `SupplierAtlas-Demo` backend (user-approved code/42-record release),
  public `SupplierAtlas-Plugin`, and the existing Atlas marketplace. Private
  credentials, original PDFs and development notes stay outside these releases.

## Public tool contract

The published content scope is engineering tables plus necessary concise typed
context. Promotional prose and supplier-history text are excluded from ingestion
and search. Original documents remain separate verification artifacts. Prefer an
established Egyptian supplier for the initial dataset; see `SOURCE_RESEARCH.md`.

| Tool | Inputs, conceptually | Returns | Boundary |
|---|---|---|---|
| `discover_catalog` | Optional category, schema detail, cursor | Available categories and coverage; for a category, defined properties, units, operators, variants and table schemas | Understand available data; does not retrieve product records |
| `search_products` | Category, optional text, typed property filters, optional related-table predicates, requested summary fields, limit/cursor | Matching product/variant IDs, names, selected fields, compact matching-row evidence | Find products; does not rank engineering suitability |
| `get_products` | Known IDs, requested sections/fields, variant selection, table IDs and row filters, limits/cursors | Requested stored product information and related rows | Retrieve known products; no broad catalog discovery |

`get_products` is the only product-detail retrieval tool. It also returns requested
technical tables and document metadata. Search and retrieval share validated
query internals; one database table does not imply one MCP tool.

Search returns model families by default, identifies the matching variant when a
variant predicate is used, and attaches the matching row when table predicates
are used. All predicates in one table condition group must hold on the same row
for the same variant. Separate table groups must be explicit; they do not imply a
shared operating condition unless a defined relation establishes one.

Text relevance helps find names and descriptions. Numeric constraints use typed
database comparisons, never semantic similarity. Unsupported fields/operators
produce actionable errors. Missing values do not satisfy numeric comparisons.

## Token-efficient response contract

- Product search defaults: IDs, readable model/variant labels, requested summary
  fields, and matching evidence. Product retrieval defaults: a compact overview
  plus a manifest of available sections/tables, not every row.
- Explicit section/field selection; units and qualifying conditions are retained
  automatically when necessary to interpret a selected value.
- Technical tables use one column definition and one common condition block,
  followed by row IDs and positional cell arrays. Required notes remain attached.
- Batch retrieval avoids repeated calls for known IDs. Pagination is scoped to
  each collection/table so one large product cannot consume the whole response.
- Initial tunable defaults: 10 search matches, at most 5 product IDs per call,
  and 20 rows per requested table. These values must be calibrated in agent tests.
- Apply a response-size budget as well as item limits. Never split a row or drop
  necessary qualifiers. Return continuation metadata or an actionable narrower-
  query error when one logical item exceeds the budget.
- Include catalog version, returned-count and continuation information. Do not
  duplicate a large JSON payload in verbose prose. Follow the selected MCP SDK's
  structured-output and compatibility requirements and measure actual client
  context consumption, including any text representation it exposes.
- A short source label and source-reference IDs accompany relevant records;
  expanded provenance/document metadata is optional within `get_products`.

## Development layout

```text
src/supplier_atlas/
  ingestion/          # Extraction adapters, normalization, validation
  catalog/            # Schemas, products, variants, definitions
  storage/            # Migrations, snapshots, parameterized queries
  query/              # Filters, projections, row relationships, pagination
  mcp/                # Three tools, bounded serialization, auth wiring
datasets/             # Reviewed import packages; originals kept out of public Git
tests/                # Reference records, query cases, MCP and agent scenarios
deploy/               # Container and cloud configuration
plugin/               # Package staging for public plugin-only release
docs/
```

There is no selection-engine module in this plan.

## Milestones and acceptance gates

### 1. Inspect the first datasheet and freeze the demo contract

- Find an official technical catalog from an established supplier in Egypt;
  choose a small product family with several variants and performance rows.
- Inventory specifications, dimensions, table headers, units, footnotes,
  configuration differences, and document revisions.
- Define table-specific versioned schemas using the actual document; products
  in one category may use different schemas and need not have identical fields.
- Create a page/table inclusion inventory: engineering data and essential notes
  retained, advertising/narrative excluded, ambiguous cells held for review.
- Prepare real lookup/filter questions with manually checked expected results.

Gate: every selected datum has an unambiguous representation, or is explicitly
excluded/pending review. Final extraction decisions require the retrieved or
supplied original file, with visual verification of selected tables.

### 2. Build and validate the first catalog snapshot

- Implement the schema in `DATABASE_DESIGN.md` and versioned migrations.
- Extract to drafts, review, normalize, and import accepted records.
- Preserve original values/units alongside normalized values and provenance.
- Detect duplicate imports by document fingerprint and stable product identity.
- Build an immutable catalog snapshot and validation report.

Gate: reference rows match the original tables; malformed or ambiguous records
cannot become published records. Rebuilding/importing does not duplicate data.

### 3. Implement the shared read/query layer and three MCP tools

- Schema discovery, product search, bounded batch retrieval, projections,
  structured filters, table-row matching, and cursor pagination.
- Parameterized queries and allowlisted property/table definitions.
- Generic response format with per-product errors in batch calls.
- Attach notes, conditions, and compact provenance without another tool.

Gate: exact lookups, model/variant inheritance, numeric filters, missing-data
handling, unit handling, same-row constraints, and pagination pass reference tests.

### 4. Evaluate the agent interface locally

- Try unknown-model search, known-model retrieval, selected fields, variant
  lookup, technical-table retrieval, cross-product retrieval, and no-match cases.
- Add adversarial cases: wrong units, ambiguous names, missing values, capped
  results, and constraints individually met only on different operating rows.
- Exercise differently shaped tables, absent optional fields, sparse rows,
  qualified measurements, repeated headers, and large paginated datasets.
- Record answer correctness, wrong-tool calls, invalid parameters, number of
  calls, response tokens, and latency. Verify that fewer tokens do not reduce
  interpretation accuracy.
- Exercise the same tool contract with a small clearly synthetic second-category
  test fixture; it is not production supplier data or an expansion of demo scope.

Gate: no critical data-integrity errors; all expected reference results are
retrievable, pagination is discoverable, and the three tools have clear usage.

### 5. Deploy the remote service and test the installed package

- Deploy pinned application/catalog versions with health and version reporting,
  credential validation, basic rate limiting, and logs that exclude secrets.
- Test protocol initialization, tool discovery, all three calls, invalid auth,
  cold start, and pagination against the deployed endpoint.
- Package manifests, MCP connection configuration, and a `use-supplieratlas`
  skill. Skill creation must follow the available skill-creator instructions.
- Install locally and verify the complete workflow in a fresh agent chat.

Gate: a client with no local backend can retrieve the expected remote data.
Record tested client/version and authentication setup; do not claim universal
client qualification.

### 6. Release through Atlas Marketplace

- Publish a versioned plugin-only release, proposed `v0.1.0-alpha.1`.
- Keep runtime source, credentials, and supplier documents out of that package.
- Add the actual released tag/commit and hosted-runtime requirements to the
  existing marketplace's `catalog.json`.
- Run its catalog generator and marketplace checks; inspect generated client
  catalogs and test installation through the marketplace.

Gate: an installed marketplace plugin completes the reference workflow. The
marketplace entry points to a verified immutable plugin release.

### 7. Expand only after the demo works

Import more products using the same pipeline, then another supplier. Additional
categories add property/table definitions and import mappings. Version schema,
catalog data, service contract, and plugin package separately. A new data release
must not require a plugin update when the public contract remains compatible.

## Pending inputs and decisions

- Initial source confirmed and imported: Alsharqa's reviewed partial catalog.
  See SOURCE_RESEARCH.md for exact files and included/excluded coverage.
- Hosted demo and single-token authentication verified; deployed configuration
  and cost-control limitations are recorded in DEPLOYMENT.md.
- Broader licensing, account isolation and additional client qualification remain
  future work. Public visibility does not grant a new supplier-document license.
- Final limits, matching syntax, and default fields: calibrate against the demo.

## Research basis

- Akeneo product model and typed values:
  https://api.akeneo.com/concepts/products.html
- Akeneo field projection/filtering:
  https://api.akeneo.com/documentation/filter.html
- Akeneo's MCP capabilities:
  https://api.akeneo.com/mcp/capabilities.html
- Akeneo table attributes:
  https://help.akeneo.com/serenity-build-your-catalog/41-serenity-manage-multidimensional-data-in-a-table
- ETIM technical classes/features/units:
  https://www.etim-international.com/classification/model-information/
- DOE explanation of ASHRAE 205 metadata and performance maps (slides 14-15):
  https://www.energy.gov/documents/bto-peer-2023-35551b-ashrae-anl-muehleisenpdf
- Agent tool boundaries, response efficiency, and evaluations:
  https://www.anthropic.com/engineering/writing-tools-for-agents
- Atlas marketplace release requirements:
  https://github.com/mroshdy91/Atlas-Marketplace/blob/main/CONTRIBUTING.md

These sources inform the design. They do not prescribe our exact three-tool
contract, and this plan makes no ETIM or ASHRAE compliance claim.
## Access-control follow-up (2026-10-15; implemented locally, deployment pending)

- Confirmed R22/R23: add request limits and email-based account registration with
  a personal token displayed on the page. The token authorizes access. Do not
  send verification emails or require proof of mailbox ownership.
- Keep the three engineering MCP tools unchanged. Onboarding belongs to the web
  interface. Email alone must not authorize access or token recovery/replacement.
- Implemented persistent per-account/global quotas and signup throttling with
  Firestore transactions; local development uses SQLite transactions. Defaults,
  accounting, schema and limitations are in ACCESS_CONTROL.md. 62 local tests
  and bounded real Firestore concurrency/persistence/revocation checks passed.
- Finish container publication, hosted verification, plugin guidance release and
  marketplace update before claiming delivery.

