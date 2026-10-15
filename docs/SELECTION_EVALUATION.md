# Engineering selection evaluation — 2026-10-15

The installed plugin was exercised through 32 native calls covering seven scoped
engineering tasks. This was a guided trial by the working agent, which already
knew the implementation. It is not a blinded independent-agent evaluation.
Requests and responses are preserved in `evaluations/selection_native_before.json`.
`scripts/evaluate_selection.py` replays them through the official MCP SDK, checks
the engineering evidence and records payload tokens in `SELECTION_EVALUATION.json`.

## Engineering outcomes

| Task and criteria | Evidence and correct interpretation |
|---|---|
| Nonperforated four-way ceiling diffuser: 100 cfm, pressure ≤15 Pa, NC ≤25, throw ≥10 ft at 50 fpm | SCD 6×6 in: 100 cfm, 0.046 inH2O (11.46 Pa), NC19, 11 ft. Candidate under the published 8 dB room-effect condition; no room-layout or final comfort verdict. |
| FlowBar: 96 L/s over 1.2 m, exact 80 L/s/m | No exact published point in the searched HT/JT tables. This does not prove the products cannot meet the duty; no interpolation was performed. |
| Separate FlowBar brief: 70 L/s ±1% over 1.2 m, ≤25 Pa, NC ≤20, 3.5–5 m throw at 0.5 m/s | HT 25 mm at 58 L/s/m gives 69.6 L/s, 18 Pa, NC16, 4 m. Conditions: 1,200 mm active length, one-way isothermal throw, 10 dB room absorption, inlet velocity <4 m/s, plenum effect excluded. |
| HT 25 mm, 36 L/s/m, NC ≤15 | Numeric search excludes the qualified NC cell. Bounded retrieval gives NC <10 and 7 Pa. The bound supports the NC comparison under its conditions; it must not be replaced by NC10. |
| Silencer 48 in, signed +1,000 fpm, IL ≥25/30 dB at 500/1,000 Hz, pressure ≤60 Pa | IL26/30 dB, but two source schedules give 0.36 and 0.211 inH2O (89.67/52.56 Pa). Cannot clear pressure criterion; supplier clarification needed. Velocity-sign meaning is unspecified. This is not a complete octave-band/noise-system design. |
| Return slot: 4 ft, 240 cfm total, 3/4 in ×2 slots, NC ≤25 | At 60 cfm/ft the source gives NC33: fails this brief. The separate 0.03 inH2O header lacks an operating airflow and cannot be paired with this point. NC assumes 4 ft length and 10 dB attenuation. |
| Fire/smoke leakage Class II at 350°F | No matching pair. Class II is published at 250°F; the 350°F row belongs to Class I. Ratings are manufacturer claims, not independently verified certification or mapped to every size/actuator. |

## Fixes prompted by the trial

1. Class-only search previously omitted the paired rating temperature. Generic
   schema `context_columns` now keeps essential applicability columns in every
   projection. The same audit retains damper height, KUL face velocity, ceiling
   dimensions and published airflow in velocity-based performance tables.
2. Empty numeric searches now explain that bounds and missing cells are excluded
   and no interpolation occurs. Numeric semantics are unchanged.
3. The three tools and their request schemas remain unchanged. No suitability
   engine, new source tool or universal product schema was introduced.

Context columns are an implementation choice supporting R08/R20. They do not add
source values or change row IDs. All 76 tables retain their full context and notes.
Tests cover declared context dependencies, source qualifications, same-row rating
pairs and the seven scenarios. Table schemas keep v1 because column meanings and
row identities are unchanged; additive interpretation metadata changes the catalog
release/hash and invalidates old cursors.

## Token measurements

Counts use `cl100k_base`, not a claim about exact billed or model-context tokens.
The JSON report separately measures the text representation and the complete MCP
result, which also contains structured content. That compatibility representation
was preserved. Schema discovery is a separate cost, reusable for the same catalog
version; this trial's 15 discovery calls total 5,342 response tokens.

| Retrieval | Filtered/projected response | Full variant table response | Reduction |
|---|---:|---:|---:|
| Qualified NC point | 588 | 1,070 | 45% |
| Two silencer schedules | 913 | 2,160 | 58% |
| Return point + pressure header | 867 | 1,370 | 37% |
| Single damper rating row | 518 | 518 | 0% |

The comparisons retain identical context, notes, source metadata and selected
cells. These are bounded variant tables, not whole-catalog comparisons.
With schema discovery already available, the successful ceiling search takes
94 request +536 response tokens; FlowBar takes 132+552. Search evidence already
answers those scoped tasks, so retrieving the same point again adds no value.

For the Class II diagnostic, the old class-only search plus temperature retrieval
cost 950 response tokens over two calls. The corrected search supplies both in
one 455-token response: 52% fewer tokens while fixing the missing context.
Some individual responses deliberately grow to preserve conditions or explain
empty results. Replaying all 32 original calls unchanged grows from 13,201 to
13,606 response tokens (3.1%); it deliberately includes the now-redundant rating
lookup. The gains above measure targeted retrieval and avoiding that extra call,
not a blanket reduction in every response. Globally minimal tokens and universal context completeness are
not established by this finite test suite.

## Efficient agent workflow

- Discover relevant category/schema once per catalog version; respect pagination.
- Convert the brief into native table axes (e.g. total flow / active length),
  retaining supplied tolerances rather than inventing them.
- Search all criteria on one published row. Stop when its evidence answers the
  scoped task; a model match is one example, not an exhaustive list of variants.
- For empty results, inspect bounds or nearby published points using bounded
  retrieval. Do not turn an empty set into an engineering rejection automatically.
- Retrieve only missing sections/columns for known IDs; batch related tables.
- Carry units, conditions, bounds, notes and unresolved source conflicts into the
  engineering answer. Broader suitability remains the engineer's task.

Local validation: 40 tests and lint pass; all 22 source fingerprints verified.
GitHub CI run 38747553950 passed tests and the constrained container check.
Hosted release `alsharqa-engineering-003+b7a55ea019a3`, Cloud Run revision
`supplieratlas-demo-00004-dfd`, serves 100% traffic. Eleven native calls covering
the seven tasks and updated schema exactly match the validated local responses;
see `evaluations/selection_native_after.json`. Hosted SDK/health/auth checks passed.
Existing cost controls were read back unchanged; see `DEPLOYMENT.md`.
