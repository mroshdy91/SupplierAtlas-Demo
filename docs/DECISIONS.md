# SupplierAtlas decisions and requirement history

Date: 2026-10-15.

## Five-reviewer PDF quality audit

- User explicitly requested five Sol subagents, intensive plugin edge cases and
  verification against actual PDFs because of possible OCR/data-quality errors (R21).
- Use fresh-context reviewers in batches, with separate report ownership. Rendered
  pages and complete applicable headers/notes are the reference; prior reviewed
  labels and passing tests are not evidence of transcription accuracy.
- All 22 local PDF SHA-256 fingerprints match freshly downloaded official files.
  This establishes source identity, not correctness of the supplier's information.
- A ceiling p.18 side-flow discrepancy has been independently confirmed: the
  21x24, one-way, 700 fpm cell is 2452, not the stored 2800. Its old source-defect
  note is incorrect. This is an import/transcription defect; OCR causation is not
  established. Corrected literal input and removed false note; stable row ID retained.
- Completed five reviews: 1,798 visual field comparisons, all 76 tables represented,
  plus exhaustive pagination and independent predicate/unit probes. Two published
  context omissions added (damper temperatures and splitter formulas); a round
  diffuser source arithmetic concern is disclosed without changing its number.
- Regression expectations come from audit ledgers, not generated catalog values.
  The new source test failed against release 003 and passes corrected 004. All 43
  tests/lint pass; report distinguishes sampling from universal accuracy.
- Skill alpha.2 removes stale SCD-only coverage and explains batch table scope and
  exact-unit boundaries. Same three tools, request schemas and numeric semantics.
- Verified delivery: runtime commit 571db65c306c80f02fcaf0aad889286427b7202a,
  Cloud Run 00005-hn8, CI 38753342609, seven native checks and hosted SDK smoke.
  Plugin alpha.2 immutable tag published by validated GitHub Actions release flow;
  marketplace pin updated with 19 checks. Existing client remains compatible.

## Engineering-selection evaluation

- User requirement R20: test the installed plugin on realistic engineering tasks,
  minimizing unnecessary tokens while retaining engineering context.
- Evidence: 32 guided native calls across seven briefs; the agent had prior
  implementation context. This is not independent or blinded agent qualification.
- Class II search lost its 250°F condition under projection. Add optional validated
  schema `context_columns`, always returned alongside row keys and requested fields.
  Audit also retains dimension/velocity/flow applicability columns where needed.
  This is additive metadata; row values, identities and the three request contracts
  are unchanged. Catalog release 003 invalidates prior cursors.
- Empty numeric results disclose scalar-only matching, excluded bounds/missing cells
  and no interpolation. Do not change qualified-value filtering silently.
- Keep compatibility text plus structured MCP output. Measure both, and compare
  bounded projected retrieval with full variant tables while asserting identical
  context/notes/sources and selected values. No blanket minimal-token claim.
- See SELECTION_EVALUATION.md/JSON for scenarios and exact measurement boundaries.
- Verified delivery: 40 tests, lint, all 22 PDF hashes, local/hosted HTTP, CI
  container checks and 11 native post-deployment calls passed. Runtime commit
  `fc65173d210529af3eda1f698e1198f0b7d2d4cd`, revision `supplieratlas-demo-00004-dfd`.
  Cost settings retained; no marketplace/plugin release or reinstall required.

## All-family engineering expansion

- Confirmed user requirement: all published Alsharqa product families, engineering
  tables and necessary context only. R19 records the scope; the three-tool contract
  remains unchanged. Advertising, history, selection verdicts and interpolation stay out.
- Implementation choice: inventory all 22 official PDFs (248 pages), render and
  review engineering pages, use OCR only as a private transcription aid. Package
  literal reviewed matrices deterministically; never ingest raw OCR during a build.
- Local result: 37 models, 758 variant/reference records, 76 tables, 3,707 rows.
  These include schedules and reference facts, not 758 independently orderable products.
  66 table pages imported, 3 repeated tables imported once, and the unlabeled VCD
  matrix withheld. Source defects and missing units are recorded in SOURCE_ISSUES.md.
- Source policy: preserve readable published anomalies with notes; make ill-typed,
  ambiguous or obscured cells unknown/excluded. Do not repair decimals, derive
  missing performance, merge conflicting size labels or combine separate ratings.
  Fire/smoke ratings are explicitly manufacturer claims, without certification verification.
- Schema choice: keep each product/table's axes and units. Preserve A/B directions,
  1–4-way patterns, signed velocities, octave bands, lengths and configurations.
  Keep incompatible/missing units unresolved; no affine temperature conversion was added.
- Response optimization: explicit table requests omit unrelated variant/table
  summaries; expanded sources are deduplicated. Keep coordinates and technical
  caveats even when projecting columns. Measured 20-row ceiling output drops from
  3,129 to 2,015 cl100k text tokens when requesting NC only, with context intact.
- Versioning: generated catalog JSON and SQLite are build outputs. Reviewed matrices
  and source inventory are versioned inputs. Existing 42 row IDs remain stable.
  Data additions require no plugin reinstall or new public tool.
- Verified: 32 local/CI tests, lint, all original PDF hashes, container checks,
  hosted SDK checks and installed native plugin discovery/search/retrieval.
  Deployed revision `supplieratlas-demo-00003-crh` serves 100% of traffic.
  Release identity and cost settings are recorded in DEPLOYMENT.md.
- Deployment hardening: the CLI's service maximum remained 1, but a new revision
  inherited a default revision maximum of 40. Set both maxima explicitly to 1
  and redeployed the same immutable image. This is an implementation choice
  supporting the user's existing free-tier requirement, not a new user rule.

## Installed plugin verified in the active chat

After the user connected SupplierAtlas and said "done", called its native
`discover_catalog`, `search_products`, and `get_products` tools successfully.
The hosted catalog identified its partial coverage and returned the requested
three-column reference row for SCD 6x6 four-way supply: 100 cfm, 0.046 inH2O,
NC19 with the 8 dB room-effect condition. This extends the earlier CLI/SDK
verification to actual tools in the user's chat. No additional data was imported;
independent agent evaluation and other-client qualification remain outstanding.

## Implementation decisions on 2026-10-15

- User confirmed Alsharqa, superseding the tentative preference for EGAT.
- Imported the visually checked 6x6, 9x9, 12x12 inch SCD slice: 21 four-way supply
  points and 21 return points. Full catalog coverage is explicitly not claimed.
- Implemented official MCP SDK 2.3, typed requests, schema-validated import,
  immutable SQLite, projected outputs, same-row filters and signed cursors.
- Numeric bounds are returned faithfully but excluded from exact numeric filters
  for this release. The limitation is discoverable in the tool and skill contract.
- Keep returned units as published; convert compatible filter units with decimal
  arithmetic. A failing mm/in equality test exposed floating-point drift and was fixed.
- Local verification: 24 passing tests, lint, stdio and actual HTTP workflows,
  plus skill validation. Token measurement includes duplicated structured/text
  wire representations, so it does not understate protocol payload size.
- User requested a new Google Cloud project with free-tier usage. Created
  `supplieratlas-demo-20261015`; user explicitly approved SDK authorization.
  Free-tier allowances and spend-cap limitations are documented in DEPLOYMENT.md.
- Remote deployment and marketplace publication were subsequently verified below.
- User requires automated future transfers rather than manual browser uploads.
  Added an allowlisted ZIP packager and a PowerShell `gcloud cloud-shell scp/ssh`
  entry point. Installed official Google CLI 584.0.0 locally after checksum
  verification; transfer, extraction, build and container tests subsequently passed.
- Actual billing report on 2026-10-15 showed 0.64 GiB-month of Artifact Registry
  storage (above the 0.5 GiB-month shared free allowance). Removed automatic
  registry creation/push from deployment; it now requires an explicit existing
  image URL. The user subsequently approved public GHCR publication.
- Container verified at 0.5 CPU / 256 MiB: expected catalog version, unauthorized
  request rejection and all three actual HTTP MCP calls passed. The test container
  and temporary test credentials were removed. Hosted checks subsequently passed.
- User approved: "Use a public GitHub container". Published only allowlisted demo
  source and 42 reviewed records to SupplierAtlas-Demo; original PDFs, project
  conversation notes and credentials are excluded. Public GitHub Actions builds
  and tests each source revision, then pushes GHCR. This supersedes the proposed
  private-backend distribution for this demo.
- Linux CI exposed SQLite ownership/permissions and uploaded CRLF shell endings.
  Fixed Docker COPY ownership and normalized public source uploads to LF. CI run
  38729268196 passed all 24 tests and actual container MCP checks.
- Deployed Cloud Run revision supplieratlas-demo-00001-bhh using the immutable
  GHCR digest. Public Cloud Run invocation permits remote clients to reach the
  application; the MCP endpoint still requires its private bearer token.
- Configured and read back a USD 0.10/month Cloud Run gross-usage spend cap with
  credits excluded. Assistant-selected conservative usage control implementing
  the user's free-tier goal; not permission to spend or a zero-charge guarantee.
- Published plugin v0.1.0-alpha.1, added its pinned commit to Atlas Marketplace,
  generated five client catalogs, and passed 19 marketplace checks. Installed
  supplieratlas@atlas-marketplace in Codex 0.162.0-alpha.17.2 on Windows. Actual
  app-server discovery verified plugin provenance, bearer auth and three tools.
  All hosted tool calls were separately verified by the official MCP SDK. No
  independent conversational-agent evaluation or universal client claim is made.
- Codex uses bearer_token_env_var in its dedicated MCP manifest; the Claude
  manifest retains header environment expansion and is not live-qualified.
  The token is configured privately in this Windows user's environment for the
  next client launch. No token is stored in any published package.

| Decision | Status / origin | Consequence |
|---|---|---|
| Product technical-data service exposed through remote MCP | Confirmed user requirement | Product data is the core asset; supplier identity is supporting metadata |
| One supplier and HVAC air outlets first | Confirmed user requirement | Prove the whole installed workflow before expanding content |
| Generic category-independent tools | Confirmed user requirement | Category differences live in schemas and data |
| Exactly three initial tools: `discover_catalog`, `search_products`, `get_products` | Explicitly accepted by user | No overlapping `query_product_data` tool |
| Query/filter published facts; agents perform engineering selection | User scope correction and accepted revised proposal | No service-side suitability verdict or supplier scoring |
| Request-shaped, token-efficient responses | Explicit user requirement | Projection, compact tables, bounded batches and visible pagination |
| Original-document references attached to product data | Accepted proposal accompanying three-tool design | No separate `get_source` in the demo; provenance retained for review/update |
| Capture requirements and update AGENTS.md as work progresses | Explicit user requirement | Maintain durable rules, decisions, and state without storing full transcripts |
| Atlas Marketplace distribution | Confirmed user requirement | Plugin-only release and generated marketplace entries |
| Python, SQLite snapshots, Cloud Run, public demo backend/public plugin | Implemented and hosted; public container explicitly approved by user | Public GHCR avoids exhausted Google registry storage allowance; credentials/PDFs stay private |
| Three-tool response defaults and generic typed-row schema | Assistant proposal based on research | Validate with the first datasheet and agent task tests |

## Request limits and personal access (2026-10-15; requirements and proposals)

- User requested stronger request limits and proposed CodeAtlas-style landing-page
  onboarding by email to obtain a personal token. Recorded as R22. No abuse or
  free-tier overage has been established by billing or request-log evidence.
- Source inspection confirms one shared bearer token and a process-local limit
  of 120 authenticated HTTP requests/minute. The counter resets with the process;
  it is neither a per-user allowance nor a persistent daily/monthly quota.
- User correction (R23): register with an email address, display a personal token
  on the page, and authorize access using that token. No outbound email or mailbox
  verification. This supersedes the assistant's verified-email proposal. Treat the
  email as unverified metadata, never as proof of identity or authority to recover,
  reveal, or replace an existing token. These are requirements, not deployed behavior.
- Proposed: individually revocable tokens stored as hashes,
  persistent atomic per-user and global quotas, burst limits, bounded signup and
  token-authentication attempts, and minimal usage telemetry. Keep the three MCP tools;
  onboarding and administrative controls belong outside the engineering tools.
- Quota accounting should distinguish MCP tool calls from protocol traffic while
  applying a separate HTTP abuse limit. Owner/test traffic must remain subject to
  the global resource budget. Choose numeric allowances from measured usage.
- Investigate rejection before the Cloud Run application and prevent origin
  bypass if adding a gateway. Application-level 401/429 responses still involve
  processing; personal tokens alone cannot guarantee zero infrastructure cost.
- Preserve the existing gross-usage spend cap. Reaching this cap is not proof
  that credits/free-tier allowances were exhausted. Check billing and traffic
  evidence before attributing a stop or charge to abuse.
- CodeAtlas's live onboarding could not be verified in this session: its web URL
  was inaccessible through the web tool and its connector required reauthentication.
  Its advertised connector metadata is not evidence of email verification.
- User subsequently authorized implementation with "Ok proceed". Implemented
  personal registration, token-only account authorization/revocation, atomic
  account/global counters and compact 429 reset guidance. No email delivery.
- Chosen implementation: the project's first/default Firestore Standard database
  in us-central1 (provider returned freeTier=true), dedicated datastore.user runtime
  identity, SQLite for local tests only. No additional paid gateway. R22/R23 do not
  fix quota numbers; initial conservative configurable defaults are documented in
  ACCESS_CONTROL.md. The existing owner token is retained but metered normally.
- Full local suite: 62 tests and lint passed. Real Firestore concurrency testing
  found read-time transaction Aborted was outside SDK commit retry handling; bounded
  whole-transaction retry fixed it, then concurrency/persistence/revocation passed.
- Last-day logs showed 558 requests (436 HTTP 200, 117 HTTP 202, five HTTP 401).
  This does not prove abuse, free-tier exhaustion or net charges. No spend-cap
  increase is authorized or made. Publication/hosted verification follows tests.

## Superseded proposals

- Initial `get_performance`, `select_air_outlets`, and `get_source` tool set was
  replaced after the user's scope correction and research.
- `query_product_data` was removed because its role overlapped with product
  retrieval. `get_products` handles requested details and technical rows.
- A server-side selection/interpolation module is not part of the current demo.

## Research interpretation

Akeneo supports a product-centered model, typed values, table attributes, selected
attribute retrieval and an MCP interface. ETIM and bSDD inform property semantics
and category definitions. ASHRAE 205 informs preservation of performance inputs
and outputs. Anthropic's tool guidance informs distinct tool responsibilities and
empirical evaluation. None of these sources mandates this exact implementation.
Links are collected in `IMPLEMENTATION_PLAN.md`.

## Historical progress before supplier confirmation (superseded)

### Additional user requirements recorded on 2026-10-15

- Search online for the initial official datasheet; prioritize an established
  Egyptian air-outlet supplier. "Most famous" remains a preference, not a verified
  market ranking or a reason to store supplier evaluation data.
- Include engineering tables and indispensable technical notes; exclude
  advertising and long narrative from the published catalog and tool responses.
- Support heterogeneous product fields/table schemas and heavy data without
  exposing additional tools or forcing a universal table layout.
- Official technical documents are being inspected; no product rows have been
  imported. A downloaded marketing cover alone is not a qualified dataset.

- Created durable guidance, revised implementation plan, and logical database
  design. No implementation, deployment, repository publication, or marketplace
  update has occurred.
- Source research completed to candidate level: EGAT proposed as the preferred
  Egyptian manufacturer to investigate; its linked diffuser PDF is cover-only.
  Alsharqa's official 28-page catalog is a verified technical fallback, with
  representative supply/return pages visually inspected. No objective popularity
  ranking was established and no final supplier choice is claimed from the user.
- Next implementation dependency: fix the initial supplier/document and validate
  every selected table and its conditions. See `SOURCE_RESEARCH.md`.
