# Five-reviewer data-quality audit

Date: 2026-10-15. Baseline: `alsharqa-engineering-003+b7a55ea019a3`.
Corrected local package: `alsharqa-engineering-004+d28b77646175`.

The user's OCR/data-quality concern was justified: the audit found one wrong
stored number and a false note attributing it to the supplier. It also found two
omissions of published engineering context and stale installed skill guidance.
The parent independently reproduced the substantive findings against rendered
original pages before making corrections. OCR causation cannot be established;
the confirmed problem is an import/transcription error.

## Independent review and measured coverage

Five fresh-context `gpt-6.1-sol` subagents ran in batches. They received the project
rules and assigned PDFs/tools, not the intended answers. They could inspect the
implementation and existing issue notes, so these are independent reviews, not
blinded scientific trials. All 22 original PDFs were fetched again from their
official URLs: remote, local and inventory SHA-256 fingerprints agree.
Source identity does not establish supplier accuracy or certification.

| Reviewer | Scope | Explicit source checks | Installed calls |
|---|---|---:|---:|
| Ceiling / fire | 3 PDFs; 19 tables | 477 visually compared fields | 14 |
| Linear outlets | 5 PDFs; 17 tables | 810 visually compared fields | 15 |
| Specialist outlets | 6 PDFs; 14 tables | 294 visually compared fields | 12 |
| Acoustics / ducts / other dampers | 8 PDFs; 26 tables | 217 visual fields; separately 360 PDF-text checks | 15 |
| API adversarial | Cross-category API; ceiling PDF spot check | Full pagination + predicate/unit probes | 15 |

The four source ledgers total **1,798 unique row/column comparisons across 494
rows**, covering every one of the 76 imported tables. Counts include coordinates
and repeated header values represented in database rows; they are not 1,798
distinct physical printed cells. The dataset has 29,635 stored cells in 3,707
rows. This was stratified sampling, not independent double-entry of every cell.
Viewing a complete page is not counted as checking every value on it.
The 360 automated sound-table comparisons supplement visual review and can
overlap sampled values; do not add them as unique visual coverage.

Reviewers reported 71 installed native calls. Full requests/responses are retained
where captured in the five JSON reports; some initial discovery calls were
inspected but not saved. All five reports disclose their individual limitations.

## Confirmed findings and disposition

| Finding | Evidence | Correction |
|---|---|---|
| P1 import error plus false source-defect note | Ceiling PDF p.18, 21x24 in, one-way, 700 fpm: published side B flow 2452 cfm; stored 2800. Stable row `alsharqa.scd.supply_patterns.r762`. Adjacent 800-fpm cell is 2800. | Corrected to 2452; removed the false note. All seven side-flow values checked. No inferred manufacturer repair. |
| P2 missing operating limits | G.S.V.D-Cat pp.3/6: AFVD and multiblade ACVD standard construction temperature limits -40 to +100 C absent. | Added typed min/max temperature context, applicability and PDF-page locators. |
| P2 incomplete splitter reference | DUCT-WORK p.14: published A/B trunk-division formulas missing from the geometry reference. | Added both literal formulas and drawing-symbol reference as context. No calculation or selection tool added. |
| P2 stale installed skill | Installed alpha.1 skill described only the old partial SCD demo. | Skill now directs agents to live discovery; clarifies batch table ownership and rounded exact-unit comparisons. Plugin alpha.2 published; existing clients need the updated package to load its revised skill. |
| Source consistency concern, not import error | Round diffuser pp.5/6: 12-inch, 300 fpm prints 225 cfm despite neck area 0.785 ft2. | Preserved 225; added a note about the disagreement with area times velocity. No fabricated corrected row. |

Only **one stored cell** changes between releases 003 and 004. All model, variant,
table and row IDs/counts remain stable. Remaining changes are necessary context
and source notes. Supplier contradictions already disclosed remain unresolved;
the audit did not authorize correcting readable supplier numbers by guesswork.

## Adversarial retrieval results

- Every row in all 76 tables traversed in 330 bounded pages with no missing or
  duplicated IDs, checked against direct read-only SQLite queries.
- 1,560 compound predicate probes matched an independent scalar-only Python
  oracle. Constraints did not combine different operating rows or variants.
- 4,752 unit-equivalence probes found no failures for mathematically terminating
  conversions. The 271 exact-equality misses involved recurring-decimal conversions
  represented by finite client inputs. Example: 900 mm =4500/127 in; finite
  35.43307086614173 in lies slightly below 900 mm. An arbitrary matching tolerance
  would change the contract; none was added.
- Eight invalid-input/budget cases rejected malformed operators, infinity,
  excessive limits, unknown fields, inappropriate numeric types, schema mismatch
  and insufficient response budgets.
- Qualified bounds, unknown cells, blanks and not-applicable values remain distinct.
  Numeric filters intentionally exclude bounds; empty-result hints explain this.
- Table requests apply to every product ID in a batch. Different table sets require
  separate calls. This is a documented usability limitation, not data corruption.

No API correctness defect was confirmed. The API reviewer measured 6,352 compact
response tokens over its 15 calls using `o200k_base`; this excludes tool schemas,
reasoning, prompts and transport wrappers. Do not compare it directly with the
earlier `cl100k_base` selection measurements.

## Regression safeguards and delivery

`scripts/build_audit_fixture.py` normalizes the independently read expectations
from the four source ledgers. It never copies expected values from the catalog.
The resulting fixture covers 1,798 fields and preserves row/table/source identity.
The new test failed on the old 2800 value before rebuilding, then passed after
the source correction. Additional tests cover the entire seven-point sequence
and projected temperature/formula context.

Local validation: **43 tests and lint passed**, all 22 source fingerprints verified.
Build outputs remain deterministic from reviewed literal input; OCR is not a
runtime/build dependency. Original PDFs, rendered images and temporary OCR stay
private. Test fixtures and compact audit reports contain engineering facts only.
Hosted release 004 is verified at revision `supplieratlas-demo-00005-hn8`, 100%
traffic. Runtime commit `571db65c306c80f02fcaf0aad889286427b7202a`, CI run
38753342609 passed tests and constrained-container checks. Seven native calls
([post-deployment evidence](audits/postdeploy.json)) match validated local responses,
comparing cursor presence rather than private signatures. Hosted SDK checks,
health and unauthenticated 401 passed. Existing cost controls were read back unchanged.
Plugin alpha.2 release commit `4459c6e20a1c8aeef1cc5424b42919041e818a9a` is pinned
in marketplace commit `611a11709a54427b4b6389565df917d67e8f6e37`; 19 marketplace
checks pass. Alpha.1 native tools were used for post-deployment checks and remain
compatible. Fresh alpha.2 installation in this active client is not claimed.
See DEPLOYMENT.md for the immutable image digest and release provenance.

## Evidence and remaining uncertainty

- [Ceiling and fire report](audits/ceiling_fire.md), [ledger](audits/ceiling_fire.json)
- [Linear outlets report](audits/linear_outlets.md), [ledger](audits/linear_outlets.json)
- [Special outlets report](audits/special_outlets.md), [ledger](audits/special_outlets.json)
- [Acoustics/ducts/dampers report](audits/acoustics_duct_dampers.md), [ledger](audits/acoustics_duct_dampers.json)
- [API report](audits/api_adversarial.md), [evidence](audits/api_adversarial.json)
- [Fresh official-source fingerprints](audits/source_fingerprints.json)

Untested individual cells may still contain errors. Exhaustive independent
double-entry remains future work. No laboratory performance verification,
certification validation, manufacturer clarification or graph digitization was
performed. The earlier passing tests established software behavior and selected
reference values; they did not establish the accuracy of every transcription.
