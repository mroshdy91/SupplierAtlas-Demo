# SupplierAtlas working rules

This file is the durable project guidance for agents working in this repository.
Read it before planning, implementation, or changing the public tool contract.
Current user instructions take precedence; update this file when the user changes
an established requirement. Do not turn an assistant suggestion into a user rule.

## Confirmed user requirements

Recorded from the project conversation on 2026-10-15:

| ID | Requirement | Basis in the user's messages |
|---|---|---|
| R01 | SupplierAtlas provides structured technical product data to connected AI agents through a remote MCP plugin. | "convert it to a structured database"; "agents to get actual data from the database" |
| R02 | Focus on products. Supplier identity is supporting metadata; supplier history, evaluation, and scoring are outside the current scope. | "not about supplier identity and history"; "this is not an evaluating the suplier" |
| R03 | Enable agents to perform engineering selection using published data. The current service retrieves and filters data; it does not issue suitability verdicts. | Engineering-selection request, followed by "this is only database" and acceptance of the three retrieval tools. |
| R04 | Start with one supplier's HVAC air-outlet data and prove the installed plugin works before expanding the dataset. | "one suplier data ... working plugin then ... adding more data" |
| R05 | Keep tools generic across product categories. Air outlets are the first dataset, not the boundary of the API. | "dont rout the tools around air outlet ... expand later" |
| R06 | The initial public tools are exactly `discover_catalog`, `search_products`, and `get_products`. | "lets go with those 3 tools" |
| R07 | Tools must have distinct responsibilities and must not overlap unnecessarily. Do not add a separate `query_product_data`, selection, comparison, or source tool without revisiting the agreed contract with the user. | "i dont want overlapping tools" and acceptance of the researched three-tool proposal. |
| R08 | Tool responses must be token-efficient and tailored to the agent's requested information. | "responc/output ... token effision ... as he required" |
| R09 | Distribute the plugin through the user's existing `mroshdy91/Atlas-Marketplace` GitHub marketplace. | User requested inclusion in their Atlas marketplace on GitHub. |
| R10 | Ground architecture decisions in professional implementations and primary documentation. Distinguish evidence from our design choices. | Request for deep online research into how professionals do this. |
| R11 | Maintain this file as work progresses and persist requirements expressed in the user's messages. | "make agents.md and update it as we go"; record the rules from messages. |
| R12 | Import engineering tables and necessary technical context only. Exclude advertising, company history, slogans, and long promotional prose. | "only ... engineering tables, not ... advertizing or long talking" |
| R13 | Accommodate different product requirements, table structures, and dataset sizes. Do not force every product into one fixed layout. | "not all the products have the same ... table structures or ... heavy data" |
| R14 | Search online for the initial dataset and prioritize an established air-outlet supplier in Egypt. Do not assert a popularity ranking without evidence. | "search for it online"; "mayeb the most famous ... supplier in egypt ... first" |
| R15 | Use Alsharqa for the demo and implement the plan using its engineering tables. | "lets use Alsharqa for the demo and start implementing the plan" |
| R16 | Create a new Google Cloud project for the hosted demo and target free-tier usage. Do not silently approve paid upgrades or claim a guaranteed zero-cost cap. | "go ... google ... yourself in a new one ... free tire" |
| R17 | Automate deployment file transfer, preferably through the CLI; future releases must not depend on the user manually uploading files. | "find other way to automaticly do that ... i will not uploead for you ... use the cli" |
| R18 | Publish the demo container publicly on GitHub Container Registry to avoid paid Google Artifact Registry storage. Backend code and the 42 demo engineering records may be public; credentials remain private. | Explicit approval: "Use a public GitHub container" |
| R19 | Expand Alsharqa coverage to all published product families, retaining engineering tables and necessary technical context only. | "add the rest of Alsharqa engineering tables"; scope clarification: "All published product families" |
| R20 | Test the installed plugin using realistic engineering selection tasks, measuring token efficiency while checking that essential engineering context is retained. | "test the plugin like an engineer doing a real selection"; "minimum tokens and no missing engineering context" |
| R21 | Use five Sol subagents for intensive plugin edge-case tests and independent comparisons with the actual supplier PDFs, focusing on data quality and possible OCR errors. | "rais 5 sol subagents"; "checking the information realibility aganist the actual pdf"; "really care about the data quality" |

## Tool boundaries

- `discover_catalog`: category coverage and queryable schema, including fields,
  units, allowed operators, variants, and technical-table definitions.
- `search_products`: discover unknown product IDs using text and structured
  filters; return compact matches and the evidence needed to explain the match.
- `get_products`: retrieve requested sections, fields, variants, or table rows
  for known product IDs, including bounded batch retrieval.
- Share internal query code where appropriate. These boundaries concern the
  agent's task, not a requirement to duplicate backend implementations.
- Do not expose unrestricted SQL or category-specific tools.

## Response rules implementing R08

- Default to compact results. Respect requested fields and sections.
- Do not dump complete catalogs, every variant, full documents, or all technical
  tables unless explicitly requested and returned in bounded pages.
- Keep units, qualifiers, applicable conditions, and explanatory table notes
  needed to interpret returned values. Token savings must not change meaning.
- Preserve model/variant/operating-row associations. Never combine different rows
  to satisfy one set of performance constraints.
- Return schema/units once per table and use compact row arrays where helpful.
  Include stable IDs and readable model names when needed for follow-up calls.
- Use opaque continuation cursors and disclose incomplete pages. No silent
  truncation; no claims of exhaustive results when more pages exist.
- Distinguish not supplied, not applicable, unknown, and not requested. Never
  substitute zero for missing data or convert a bound such as `<20` into `20`.
- Source references are attached metadata; no extra source lookup is required
  during the normal retrieval workflow.
- Measure response size and correctness in evaluations; do not equate fewer
  tools or fewer characters with success without evidence.

## Engineering-content and flexible-schema rules

- The published catalog contains engineering tables and concise typed facts
  needed to identify or interpret them. Retain units, symbols, applicable sizes,
  configurations, test conditions, qualifiers and essential footnotes.
- A full original PDF can be retained privately for verification, but its
  advertising and general narrative must not enter product search or MCP output.
- Products may have different optional fields, zero or many technical tables,
  and different schemas within the same category. Validate each table against
  its own versioned schema; do not require a universal set of performance fields.
- Handle scalar values, ranges, qualified values, sparse tables, repeated
  operating points, and multi-axis data without losing their relationships.
- Heavy datasets are described first and retrieved by filtered bounded pages.
  Large arrays, source documents and diagrams must not be in default responses.
- Search timestamps and URL upload directories are not document revision dates.
  Store the actual printed revision/date when present, otherwise unknown.

## Maintaining project memory

At each meaningful change:

1. Identify new explicit user requirements and corrections in the conversation.
2. Update this file's requirement table or rules without duplicating entries.
3. Record important decisions and their origin in `docs/DECISIONS.md`.
4. Update the implementation plan and database design if affected.
5. Separate confirmed requirements, proposed defaults, implemented behavior, and
   verified behavior. Never describe a plan as already built or tested.

Preserve a short history for superseded decisions. Do not record credentials,
unrelated personal information, or entire chat transcripts here. If a preference
is ambiguous, record it as an open question rather than inventing a rule.

## Current project state

- R21: five fresh-context Sol reviews completed. All 22 fresh official PDF hashes
  match. Visual ledgers cover 1,798 row/column comparisons across 494 rows and all 76
  tables; this is sampling, not exhaustive transcription verification. API probes
  cover all 3,707 paginated rows, 1,560 compound predicates and 4,752 unit conversions.
  One import error (SCD p18 side flow 2452 vs 2800), its false source-defect note,
  two context omissions and stale skill coverage were independently reproduced.
  Release 004 fixes these; 43 tests/lint, CI container checks, hosted SDK and seven
  post-deployment native calls pass. Plugin alpha.2 is published and marketplace
  pinned; installed alpha.1 remains wire-compatible, but has old skill text until updated.
  See docs/DATA_QUALITY_AUDIT.md and the five ledgers. No claim of zero remaining errors.
- Engineering-selection evaluation (R20): 32 guided native calls across seven
  scenarios exposed a projection gap (Class II temperature) and an empty-result
  interpretation trap. Generic validated `context_columns` now survives projections;
  numeric empty results explain excluded bounds/missing cells without changing matching.
  Local catalog `alsharqa-engineering-003+b7a55ea019a3` retains all counts and row IDs.
  See `docs/SELECTION_EVALUATION.md` for evidence, token measurements and limitations.
  40 tests, lint, local/hosted HTTP, CI container checks and 11 post-deployment
  native calls passed. Guided tasks are verified; independent-agent qualification
  is not claimed. Context dependencies are declared on 16 schemas.
- Expansion delivered (2026-10-15): all 22 published Alsharqa catalog families
  reviewed (248 PDF pages). Hosted package has 37 models, 758 variant/reference
  records, 76 technical tables and 3,707 rows. Original 42 SCD rows/IDs preserved.
  Table-page audit: 66 imported, 3 duplicate tables imported once, 1 unlabeled VCD
  matrix withheld. Obscured ACVD cells and unusable source cells remain unknown or
  explicitly excluded; no graph digitization or silent source repair.
- Expanded validation: 43 tests, lint, all 22 PDF hashes, cross-family reference
  cells, complete pagination, response budgets, local HTTP and CI container checks
  passed. Hosted SDK checks and the installed plugin's three native tools passed.
- Live catalog `alsharqa-engineering-004+d28b77646175`, revision
  `supplieratlas-demo-00005-hn8`, 100% traffic. Runtime commit
  `571db65c306c80f02fcaf0aad889286427b7202a`, CI run `38753342609`.
  Image digest `sha256:8054376b80b631fedbe4996f4cb812802061ded025f19c68dc09c005e27074d6`.
  Plugin v0.1.0-alpha.2 tag/commit `4459c6e20a1c8aeef1cc5424b42919041e818a9a`;
  marketplace commit `611a11709a54427b4b6389565df917d67e8f6e37`. The data fixes
  work with existing alpha.1; alpha.2 updates client guidance only.
- Cost controls retained: scale-to-zero, service max 1, 0.5 CPU / 256 MiB,
  concurrency 1, timeout 30, throttling on and startup boost off. Deployment script
  now explicitly sets revision max 1 as well as service max 1. Existing spend cap
  was not raised. Public GHCR/Actions remain the build/publication path.
- New data uses table-local versioned schemas. Do not assume product-level fields
  are populated for every category; discover and filter the relevant table schema.
- Explicit row requests omit unrelated variant lists/table summaries; expanded
  row sources are deduplicated by ID. Table context, notes and coordinates remain.
- `datasets/alsharqa/prepare.py` packages reviewed literal matrices. Generated
  `catalog.json`/SQLite are build outputs. OCR drafts and original PDFs are private
  inspection aids, not build inputs. `audit.py` regenerates coverage/source notes.
- See `docs/ALSHARQA_COVERAGE.md` and `docs/SOURCE_ISSUES.md` for the expansion.

### Initial release history (superseded dataset coverage)

- Implementation underway. Alsharqa is now the user-confirmed demo supplier.
- Initial reviewed slice: SCD nominal 6x6, 9x9 and 12x12 inch sizes; four-way
  supply (p.9) and return (p.19, notes p.20), 42 operating records total.
  Other patterns and sizes remain outside the initial imported coverage.
- Implemented with official Python MCP SDK 2.3, validated import packages and
  read-only SQLite snapshots. Exactly three tools work over stdio and HTTP.
- Verified: 24 tests, lint, actual local HTTP client workflow and skill validation.
  Token measurements are in `docs/EVALUATION.json`; these are deterministic tool
  tests, not an independent agent evaluation. Installed-client qualification is
  recorded separately below.
- Created Google project `supplieratlas-demo-20261015` (524685338738). User
  explicitly approved Google Cloud SDK authorization and public GHCR publication.
- Local Google CLI authorization, automatic SCP upload, remote extraction, Docker
  build and container HTTP checks verified. `deploy/cloudshell.ps1 -BuildAndTest`
  works without manual uploads. Container checks passed at 0.5 CPU / 256 MiB.
- Live Cloud Run service: `https://supplieratlas-demo-524685338738.us-central1.run.app/mcp`.
  Revision `supplieratlas-demo-00001-bhh`, public invocation with application bearer
  authentication. Hosted health, unauthenticated 401, all three tools and reference
  engineering data verified. Public image is pinned by digest; no Google registry
  repository or Cloud Build job was created.
- Request-based billing, min 0 / max 1, 0.5 CPU / 256 MiB, concurrency 1. A USD 0.10
  monthly Cloud Run gross-usage spend cap is CONFIGURED, excluding credits. This is
  a conservative usage control, not a paid-spend allowance or guaranteed zero-cost
  cutoff; enforcement delay and shared free-tier allowances still apply.
- Published `mroshdy91/SupplierAtlas-Demo` runtime and `SupplierAtlas-Plugin`
  release `v0.1.0-alpha.1` (commit `7227beee72a9103acf595bd8f27df60a8506723b`).
  Added the pinned release to Atlas-Marketplace, commit
  `1425615c5ca82963dfe26f40fce193438987bbb4`; 19 marketplace checks passed.
- Codex 0.162.0-alpha.17.2 on Windows installed the plugin, authenticated and
  discovered exactly three tools. Other clients and fresh conversational agent
  behavior remain unqualified. The private token is configured in this user's
  environment; a new client process is required to inherit it.
- Preferred repeat deployment is `deploy/deploy.ps1 -Image <immutable GHCR digest>`.
  GitHub Actions builds/tests/publishes automatically; manual uploads are obsolete.
- After the user connected the installed plugin, all three native SupplierAtlas
  tools were successfully called from this chat on 2026-10-15. Discovery, product
  search and projected retrieval returned the expected 6x6 four-way supply row
  (100 cfm, 0.046 inH2O, NC19 with 8 dB room effect). This confirms live chat
  integration; it is not an independent agent evaluation or other-client qualification.
- See `docs/IMPLEMENTATION_PLAN.md`, `docs/DATABASE_DESIGN.md`, and
  `docs/DECISIONS.md` for the current design and research basis.
