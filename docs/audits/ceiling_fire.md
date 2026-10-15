# Ceiling diffuser and fire damper source audit

2026-10-15. Read-only production audit; no data corrected. Original PDFs rendered using PyMuPDF and viewed as complete pages, including headings, diagrams and notes. The 477 individually recorded comparisons in `ceiling_fire.json` use manually read published cells rather than assuming the reviewed matrices are correct. 476 matched and one did not. This is stratified verification, not an exhaustive cell audit.

## Confirmed error (P1)

`ceiling-diffusers.pdf`, PDF/printed p.18: SCD 21x24, one-way pattern, 700 fpm, side airflow B prints **2452 cfm** (printed `-2452`; the leading dash denotes absent direction A). Local SQLite and installed native service return **2800 cfm**, row `alsharqa.scd.supply_patterns.r762`. The table note incorrectly calls 2800 a published inconsistency. Correct the literal matrix and remove this false example from its note. The 800-fpm cell is 2800; no manufacturer clarification is needed to read these cells.

Reproduction:

```json
{"request":{"ids":["alsharqa.scd"],"tables":[{"table_id":"alsharqa.scd.supply_patterns","filters":[{"field":"size_label","value":"21x24"},{"field":"ways","value":1},{"field":"neck_velocity","value":700}],"limit":1}],"include_sources":true}}
```

Full-resolution evidence: `tmp/audit_ceiling/p18-full-3x.png`. All seven one-way side-flow cells independently checked: 871, 1053, 1400, 1748, 2100, 2452, 2800. Total-flow row matches this series. Surrounding 700-fpm four-/three-way side flows and throw endpoints and two-way side flow/throw also match the database. No surrounding systematic column shift was identified.

## Source defects distinguished from errors

- SCD p.9 reversed throw 15-12 and 21-19; pp.10-17 further reversed/nonmonotonic data remain literal. These are visible source defects, not evidence of a database error.
- P.12 6x18 cells `-94` in a throw row and `13-18` in the following side-flow row are visibly misplaced. Database unknown handling and explanatory note are appropriate.
- P.14 middle block prints 6x21 left and 9x21 right and first total 63; source ambiguity is represented explicitly.
- P.19 return prints **8x18** beside 2.25 ft2. Literal size is preserved, with warning.
- SCDP pp.22/23 pressure at 600 fpm visibly prints **0.94**, not 0.094. Database and native projection preserve 0.94 with warning. P.22 supply 9x9 area 0.5 differs from return p.24 0.56. Single `2` throw for 6x6 one-way 250 fpm is appropriately unknown at both terminal velocities.
- SFD p.4 construction text 1.6 mm frame differs from 20-gauge drawing. P.5 retaining angles 38x38x2 and M5 text differ from diagram 40x40x3 and 6 mm; sleeve projection 152 versus 150 mm. These are visible source conflicts, disclosed in output. P.6 vertical 27x41 inches paired with 672x1026 mm is inconsistent; published inch limits remain distinct.

## Coverage and installed-service checks

Complete rendered relevant pages inspected: ceiling pp.9-24 (16 pages); motorized fire/smoke pp.2 and 6-13 (9 pages); SFD pp.4-6 (3 pages), total 28 pages. Stratified checks span every additional SCD supply source page and block, both additional-return pages, SCDP supply/return/construction, all five series rating tables, all four fire/smoke dimension schedules, and all three SFD tables. JSON records exact table, row ID/key, column, published and stored values. Larger ceiling tables sample first/middle/last operating columns; not every throw or side-flow cell was counted.

Fourteen installed native calls exercised catalog discovery, category search, schemas, projected Class II leakage (250 F survives), source-expanded bad row retrieval, entire one-way series, SCDP abnormal pressure, ambiguous throw, numeric bound exclusion and blank damper schedule tails. Blank 800-mm SFSD30 height/blades remain `not_supplied`; no invented blade count. NC `<18` is excluded by numeric `<18` and the empty-result hint explains this. Cross-product request containing each product's different table ID returns per-product ownership errors; corrected single-product request succeeds (documented invocation constraint, not transcription error).

All assigned PDFs are readable for sampled engineering tables; the source itself contains consequential defects. Existing notes and passing tests cannot replace looking at the published page: this audit found a fabricated source-defect note masking a wrong stored cell. No suitability or certification conclusion was attempted. Unviewed front matter, wiring pp.3-5 and uncounted individual cells remain outside verified coverage.
