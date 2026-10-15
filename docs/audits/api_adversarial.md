# Independent API adversarial audit

Reviewer five, 2026-10-15. Baseline: `alsharqa-engineering-003+b7a55ea019a3`.
No production edits or deployment performed. Reproducible installed-native requests,
responses, response byte/token counts and local-check summaries are in
`api_adversarial.json`; local scripts and detailed sweep output are under
`tmp/audit_api/`.

## Result

No API correctness defect was confirmed in this review. One installed-skill
documentation defect is confirmed: the skill still states the catalog is only a
partial SCD demo, whereas native discovery reports 22 catalogs and 37 models.
Severity P2 documentation: a fresh agent may incorrectly limit its retrieval scope.
The live tool's coverage disclosure itself is current. Parent notified separately.

## Installed plugin checks

15 bounded native calls, beginning with fresh discovery, returned 6,352 response
tokens measured locally using `o200k_base` on compact structured JSON. This is a
tool payload metric; it excludes schemas, reasoning, prompts and transport wrappers.

- Discovery led to category properties and the supply table schema before numeric queries.
- 152.4 mm neck-width equality found the six-inch variant. 47.19474432 L/s
  retrieved the exact 100 cfm point, preserving pressure 0.046 inH2O and NC19.
- Width6 plus height9 produced no match; independently matching different variants
  did not manufacture a candidate.
- 63 cfm plus pressure >=0.2 produced no match; constraints did not combine rows.
- Projecting NC retained airflow coordinates, units, pattern, 8dB room effect and
  notes. The first two published cells remained structured `<18` bounds.
- 100 cfm plus NC<=18 returned no scalar match with the explicit bounds/missing
  explanation. Numeric bound exclusion matches the published contract.
- Mixed existing and nonexistent IDs returned valid rows plus a per-ID error.
- One-row continuation advanced 63 to75cfm without duplication. Reusing the same
  cursor with the 9x9 product failed explicitly.
- Unknown schema, incompatible airflow pressure unit and unknown projected column
  failed explicitly without returning misleading data.

## Independent local checks

Read-only SQLite was the oracle, independently querying row IDs and scalar values.
The public query implementation was then exercised through validated request models.

- All 76 tables, 3,707 rows: 330 bounded pages at13rows each exactly matched direct
  ordered SQLite IDs, with no duplicate or missing rows.
- 1,560 compound same-row numeric queries across table schemas matched a Python
  scalar-only predicate oracle, including strict/inclusive/equality operators.
- 4,752 unit-equivalence probes: 271 recurring-decimal client round trips missed
  exact equality; zero failures involved a mathematically terminating conversion.
- Eight validation cases correctly rejected unsupported operators, infinity,
  excessive row limits, SQL-shaped unknown field names, boolean/string numeric
  predicates, schema/category mismatch and a deliberately insufficient byte budget.

The 271 round-trip misses are a precision caveat, not a confirmed defect. For
example, 900mm equals4500/127in exactly. The finite client value
35.43307086614173in is slightly below900mm; exact equality therefore need not match,
and an inclusive upper-bound request can exclude900mm legitimately. No arbitrary
engineering tolerance should be introduced to hide this. Use native-unit filters
or an explicitly meaningful engineering interval when a conversion is rounded.

## Original PDF check

Fresh SHA256 of `data/sources/alsharqa/ceiling-diffusers.pdf` matched the source
metadata: `6548714c85b082cda1206210774a42baea2fd164b7e1a39058a977e9c50e57df`.
Rendered PDF/printed page9 with Poppler and visually inspected the complete page.
The six-inch four-way points63/75/100cfm show pressure0.018/0.026/0.046inW.G. and
NC<18/<18/19, respectively, agreeing with retrieved data. The page's notes state
8dB room effect, nominal inches, square-foot neck area and throw terminal velocities
100/50fpm; returned context preserved these meanings. Render retained at
`tmp/audit_api/ceiling-p9.png`.

## Limits

Only one original PDF page was visually checked here; broad source verification
belongs to the other four reviewers. Hosted behavior was sampled in15calls; the
exhaustive sweeps were local and do not establish load, concurrency or rate-limit
reliability. Unit sweep used one alternative compatible unit per native unit.
Product-binding of a native cursor was checked; comprehensive cursor tampering
and every query mutation were not tested. This audit does not certify every
source cell or infer engineering suitability.
