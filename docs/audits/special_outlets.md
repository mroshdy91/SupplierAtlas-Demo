# Special outlets source audit

Audited six PDFs and all 14 imported table definitions (689 stored rows in scope). Viewed 17 complete rendered table pages, including the duplicate SDL table in Jet-diffusers p.7. Explicit sample ledger: 42 first/middle/last rows, 294 value fields including row keys; all 42 also agree between catalog JSON and SQLite. This is stratified sampling, not exhaustive verification of 689 rows.

No transcription error was confirmed in those samples. See `special_outlets.json` for exact rows, values, source locators, and native requests/responses. The ledger is a catalog snapshot manually compared against page images, not independent OCR ground truth.

## Finding SO-01: published flow consistency concern

Round-diffusers PDF p.5, SRD supply, 12-inch neck / 300 fpm, airflow column: source, JSON, SQLite and native plugin all return **225 cfm** (`alsharqa.round-diffuser.supply.r31`). The same printed flow occurs in RRD return on p.6 (`alsharqa.round-diffuser.return.r31`). Published neck area is 0.785 ft²; area × velocity gives 235.5 cfm, while the next 400 fpm point prints 315 cfm, consistent with 314 calculated. This warrants a source-consistency note or supplier clarification, not changing the faithfully transcribed 225.

Full p.5 image: `D:/Personal/playGround/SupplierAtlas/tmp/audit_special_outlets/Round-diffusers-5.png`.

## Units, symbols, footnotes and anomalies

- ABJD p.4 explicitly says dimensions are mm; catalog correctly assigns mm. Its p.5 defines CFM, pressure in in.w.g., and neck fpm, but does not define throw units, terminal velocities or Ak units. Native output correctly retains these as unknown rather than borrowing SJD conventions. Nonmonotonic 16-inch throws and `>50` NC remain literal.
- SJD p.4 says all dimensions are mm; sampled single/multiple-panel sizes match. Source anomalies (150-4P duct width 400, 250-2P duct width 400, 350-2P/3P A=1040/1530) are preserved and noted. P.5 specifies throw at 0.25 m/s and 10 dB room attenuation, correctly retained by column name and context. Factor-ten SI cells are unknown with the printed values in notes. Pressure reversals remain literal.
- SDL Drum p.3 and duplicate Jet p.7 define m/s neck velocity, mm H2O static pressure, throw in meters at **0.75, 0.5, 0.25 m/s**, and 10 dB room attenuation. Column identities preserve all three terminal velocities. Alternative neck sizes remain a single source group. The printed 1363 cfm first point is preserved and flagged.
- Disc p.4 does not print a dimensional unit; absence is disclosed. Pp.6/8 define total pressure in mm H2O, 10 dB room attenuation and +10/0/-10 disc position below/normal/above; native results retain this. Pp.5/6 suspect 30.6 and 16.3 pressure cells are withheld as unknown with the printed values disclosed. Blank cells remain not supplied, not zero. Literal bounds remain bounds.
- Swirl p.5 provides mm dimensions; p.7 defines pressure in inches of water, CFM, Ak ft², 10 dB absorption and dash NC as `<15`. Retained correctly. Throw feet are printed, but terminal velocities are absent; native output says so. Vertical/horizontal axes remain distinct.
- Round dimensions p.7 preserve the supplier's paired inch/mm sizes, explicitly not exact conversions. Performance pp.5/6 define neck area ft², velocity fpm and velocity pressure inch W.G.; total-pressure unit is not separately stated. It stays unspecified. Throw feet remain printed order with terminal velocity unknown; room attenuation is unknown. Diagram-only dimensions 45 and 5 are not imported in the table; this is not a transcription error in imported cells.

## Live installed-plugin checks

Twelve native calls: category discovery, jet model search, disc schema discovery, then nine saved edge calls. Verified unknown versus blank versus bound; scalar-filter exclusion hint; SJD SI unknown; ABJD `>50`; swirl dash conversion; SDL grouped size and anomalous 1363; round 225 and unspecified pressure unit. Stable row keys and technical context survive narrow projections.

The twelfth call deliberately batched ABJD and SJD with two different table IDs: both products returned `Requested table does not belong to this product`. Table requests apply to every product ID; unlike table sets require separate calls. This is a usability limitation, not a source-data mismatch. No suitability verdict was requested or produced.

## Reproduction and limits

Full native requests and responses are embedded in JSON and `tmp/audit_special_outlets/live_calls.json`; three initial calls were inspected but not saved in full. Sampling script and PNGs are in `tmp/audit_special_outlets/`. Every imported table has three explicit samples. Entire page inspection includes headers and footnotes, but does not establish every table cell is correct. No source correction, interpolation, independent laboratory verification, or production change was performed.
