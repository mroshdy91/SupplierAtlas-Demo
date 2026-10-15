# Linear outlets independent PDF audit

Audited catalog `alsharqa-engineering-003+b7a55ea019a3` on 2026-10-15. No numeric import error or material missing performance context was confirmed in the checked sample.

## Scope and evidence

Five original PDFs were rendered with PyMuPDF at 1.6x and their complete relevant table pages were **viewed**, including headers and footnotes. Overview contact sheets of the other pages were also inspected. Viewing a page is not counted as checking every cell.

The machine-readable ledger in `linear_outlets.json` contains **211 distinct operating/reference rows and 810 individually compared published values** across **all 17 assigned imported tables**, containing 1,170 database rows. Every ledger entry names table, physical PDF page, row ID, coordinates, published values and actual SQLite values. All 810 agree. These are stratified samples, not a full independent double-entry of 1,170 rows. Source literals were read from the actual rendered page; existing `reviewed_*.py` labels were not accepted as proof.

| Source | Complete relevant physical PDF pages viewed | Tables | DB rows | Sampling emphasis |
|---|---|---:|---:|---|
| Flow-Bar-Diffuser.pdf | 6–8 | 4 | 48 | Each HT/JT slot opening, first/middle/last operating column, all dimensions |
| Linear-slot-diffuser.pdf | 10–14 | 4 | 320 | Both widths; first/central/last slots and operating points; fractional dimensions; standalone pressure headers |
| Linear-bar-grilles-_-registers.pdf | 9–12 | 4 | 252 | Every model and width at 400/800/1600 fpm; pressure, flow, NC, throw endpoints and Ak |
| Light-troffer-diffusers.pdf | 6–7 | 3 | 215 | Every fixture length, round/oval/LP shapes, first/central/last duty regions, NC dashes and velocity-pressure references |
| Grilles-_-registers.pdf | 10–13 | 2 | 335 | Every performance size group at first/middle/last velocity with different angles; range-table extrema; duplicate p12 |

## Source defects and ambiguous source data

These are **source defects or limitations, not discovered import errors**:

- Light troffer p7, three-foot fixture at 160 cfm: printed throw is `7-11-51 ft`; all four neck options retain 51 with a warning. Terminal velocities and total-pressure units are not printed on these performance tables and are not inferred from the separate velocity-pressure reference.
- Grilles p13, 24x24 at 500 fpm/0°: throw really prints 38 ft between 51 and 66. Database retains 38 with warning.
- LBG-0Y p10, three-inch width: source Ak really prints 0.97 ft²/ft. Database deliberately withholds the physically suspect number as unknown; note retains the published value and reason. The 12-inch/800 fpm throw 37–39 is also printed.
- Linear-slot p13–14 pressure values sit in a header without a specific flow-row association. Database correctly keeps them in a separate reference table and explicitly forbids pairing them with arbitrary flow. The unusual smaller one-inch Ak series is printed, retained and warned.
- Grille p12 repeats p11; importing it once is correct.

## Engineering interpretation checked

Flow-bar output preserves L/s/m, 1,200 mm NC/throw reference length, 10 dB absorption, isothermal terminal velocities 0.8/0.5/0.3 m/s, inlet velocity <4 m/s, absence of plenum effect, and one-way/divided-flow instructions. Throw factors are 0.72 for 600 mm, 1.7 for 3,000 mm and 1.8 for 3,600 mm; no calculated rows are asserted. JT supply-as-return NC+3 remains a note.

Linear-slot output preserves CFM/ft, NC on a four-foot unit with 10 dB attenuation, horizontal supply throw at 100/50 fpm, vertical NC-5 instruction and return deflection-blade configuration. LBG output preserves airflow/Ak per foot, eight-foot throw length, 100/50 fpm endpoints, 8 dB room effect and supply without damper; its pressure is total pressure. Grille output preserves shared size groups, angle-specific static pressure/throw and a single size/flow NC series; missing terminal velocity/attenuation are explicitly disclosed. No material missing interpretation context was confirmed.

## Installed plugin edge cases

Fifteen native calls exercised discovery, searches in all five categories, schema inspection, projected/filtered retrieval, missing values, source expansion and bounded pagination. Saved requests/results are in the JSON ledger. Key results:

- JT 25 mm at 31/62 L/s/m returns separate 2/7 Pa rows with `<10` NC, shared context and correct PDF7/printed6 locator.
- Projected SLT three-foot/160 cfm retrieval keeps fixture/shape/flow coordinates, anomalous 51 ft and source warning.
- Projected LBG-0Y three-inch data returns unknown Ak, bounded NC and an explicit continuation cursor.
- A slot 0.75-inch/one-slot/10 cfm/ft numeric NC≤20 search returns empty because `<20` is a bound, with an explanation. It does not falsely claim unsuitable.
- A flow-bar query demanding the 122 L/s/m row and pressure≤7 Pa returns empty: different operating rows are not combined.
- Projecting only a return pressure header retains slot coordinates and the missing-operating-flow warning.

A batch containing three different models and their three distinct table IDs returns a table-ownership error for each product. Split model/table requests work. This is an API usability limitation, not evidence of source corruption. One failed batch request is recorded in abbreviated form; the successful split requests preserve full predicates and results.

## Limitations

Sampling cannot establish that every source cell is correct. No independent interpolation, graph digitization, unit-conversion stress test, or suitability decision was performed. Generic room recommendation/conversion tables and dimension drawings were screened for coverage but not entered into the product-performance checks. The supplier PDFs remain the evidence; the renders and reproduction scripts are under `tmp/audit_linear/`. No production data or code was changed.
