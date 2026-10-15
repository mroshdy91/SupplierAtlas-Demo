# Published-source qualifications

These are source limitations and interpretation notes retained with the data. Manufacturer clarification remains necessary for ambiguous or contradictory values. No guessed corrections or interpolation were substituted.

Unreadable/ill-typed cells are unknown; genuine blanks are not supplied; absent directions are not applicable. Readable suspect numbers remain literal with notes. Units are unspecified where the source does not establish them.

## Access-door.pdf

**alsharqa.access-door.dimensions**

- The 12x12 row prints B=42 inches. B is withheld as unknown pending supplier clarification; no correction to 12 is inferred.

## Air-louvers.pdf

**alsharqa.air-louver.pressure**

- Negative intake pressures are the source sign convention, not corrected to positive losses.
- The source does not identify the filter thickness used for this pressure table; do not assume all filter options have identical losses.

**alsharqa.air-louver.effective-area**

- The matrix contains small asymmetric values; source rounding and discrepancies are retained. No interpolation is performed.

**alsharqa.sand-trap-louver.effective-area**

- Height and width are independent axes. The published matrix is asymmetric; dimensions must not be swapped.

## DUCT-WORK.pdf

**alsharqa.rectangular-duct.construction**

- Single-wall material options: galvanized steel, stainless steel, aluminum, painted galvanized steel.
- Acoustic double-wall outer options: galvanized, stainless, black steel, aluminum or painted steel; inner perforated options: galvanized or black steel.
- Thermal double-wall inner and outer options: galvanized, black steel, aluminum, stainless or painted steel. No standard insulation thickness/density is specified for that construction.

**alsharqa.rectangular-duct.liner-fastening**

- A/B/C/E refer to the source fastening diagram. Their table does not print a unit; values remain unit-unspecified rather than silently converted.

**alsharqa.branch-takeoff.dimensions**

- The source recommends sealant after installation. Rectangular takeoffs can have a splitter damper and acoustic lining/double walls; round takeoffs can have double walls.
- The 80–315 mm diameter interval is a published range, not a list of discrete available sizes. Other round diameter schedules are referenced but not provided in this PDF.

**alsharqa.duct-hardware.cleat-section**

- Dimension names describe positions in the source section sketch; no sheet thickness is specified for the cleat.

**alsharqa.splitter-damper.dimension-rules**

- Symbols refer to the source branch sketch. No calculated dimensions, flow split or pressure-loss coefficients are supplied by this table.

## Fire-Damper-.-.pdf

**alsharqa.sfd.construction**

- The text specifies a 1.6 mm frame, while the drawing says 20-gauge GI casing. These descriptions conflict and must not be treated as equivalent.

**alsharqa.sfd.installation-limits**

- The source pairs vertical 27x41 inches with 672x1026 mm, which is not an exact conversion. Only the printed inch limits are used here; no corrected metric rating is invented.
- These are published product limits, not independent confirmation of listing, installation compliance, or suitability.

**alsharqa.sfd.installation-details**

- The text specifies retaining angles 38x38x2 mm, while the diagram shows 40x40x3 mm and 6 mm bolts. This unresolved difference is disclosed rather than merged.
- Sleeve projection is 152 mm maximum in text, 150 mm in the diagram.
- PDF p.6 specifies opening clearance 1/4 inch larger up to 24-inch dampers, plus 1/8 inch per additional linear foot. Follow the damper airflow arrow and provide inspection access; these are supplier instructions, not a substitute for an approved installation detail.

## G.S.V.D-Cat.pdf

**alsharqa.afvd.dimensions**

- Rows preserve the published width/height/blade schedule; they do not assert an exhaustive set of orderable width-height combinations.
- The p.3 narrative says single blade up to 300 mm height, while the p.4 table lists two blades at 300 mm; the table is retained with this conflict disclosed.

**alsharqa.acvd-multiblade.dimensions**

- Rows preserve the published width/height/blade schedule; they do not assert an exhaustive set of orderable width-height combinations.
- A blue block obscures the lower part of the published schedule. Hidden cells are not inferred.

**alsharqa.acvd-round.diameters**

- The same diameter schedule is also published in Round Volume Damper PDF p.4; it is imported once.

## Grilles-_-registers.pdf

- PDF p.12: Same performance table as p.11; imported once.

**alsharqa.supply-grille.size-flow-range**

- These are the supplier's overview ranges, not verified duty points or suitability limits. Some detailed performance rows fall outside them.

**alsharqa.supply-grille.performance**

- PDF p.12 repeats p.11; imported once. Each listed size group shares the published performance series.
- The 24x24 group at 500 fpm and 0 degrees prints throw 38 ft, between 51 and 66 ft. That non-monotonic source value is retained without correction.
- Ak, airflow and velocity do not always satisfy a consistent conversion in the source. They are transcribed independently; no recalculated values replace them.

## Jet-diffusers.pdf

- PDF p.7: Same drum performance as Drum-Diffuser.pdf p.3; imported under SDL once.

**alsharqa.sjd.multiple-panel**

- Values are as printed. SJD150-4P duct width 400, SJD250-2P duct width 400, and SJD350-2P/3P face widths 1040/1530 depart from adjacent patterns. Confirm these dimensions before fabrication; no correction is inferred.

**alsharqa.sjd.performance**

- Three SI airflow cells conflict by about a factor of ten with their CFM cells: 100 mm at 4/7 m/s prints 0.378/0.614 m3/s; 150 mm at 4 m/s prints 0.756. These SI cells are unknown pending clarification; CFM remains as printed.
- Non-monotonic static-pressure values at 300 and 400 mm, and the 400 mm NC progression, are preserved as printed. Published rows are not a fitted performance curve.

## Light-troffer-diffusers.pdf

**alsharqa.slt.single-side**

- Throw terminal velocities, total-pressure units and NC room attenuation are not specified on these performance pages.
- NC dashes have no defined numeric threshold in this catalog and remain not supplied.
- The p.4 narrative describes round inlets while this performance table labels the neck oval; the performance labels are retained.

**alsharqa.slt.dual-side**

- Throw terminal velocities, total-pressure units and NC room attenuation are not specified on these performance pages.
- NC dashes have no defined numeric threshold in this catalog and remain not supplied.
- The 3-foot fixture at 160 cfm prints throw 7-11-51 ft; this anomalous triple is retained as printed, not corrected to 15.

**alsharqa.slt.velocity-pressure**

- Repeated on p.7; imported once. Dashes remain not supplied. This reference table does not state oval/round shape or fixture length.

## Linear-bar-grilles-_-registers.pdf

**alsharqa.lbg-0.supply**

- Airflow and Ak are per foot of run; throw is for an eight-foot grille, as printed in the footnote.

**alsharqa.lbg-0y.supply**

- Airflow and Ak are per foot of run; throw is for an eight-foot grille, as printed in the footnote.
- The 3-inch LBG-0Y Ak prints 0.97 ft2/ft, exceeding its gross face area; it is withheld as unknown. The 12-inch/800 fpm throw 37–39 ft remains as printed.

**alsharqa.lbg-15.supply**

- Airflow and Ak are per foot of run; throw is for an eight-foot grille, as printed in the footnote.

**alsharqa.lbg-30.supply**

- Airflow and Ak are per foot of run; throw is for an eight-foot grille, as printed in the footnote.
- The 3-inch/1200 fpm throw prints 22–23 ft; it is retained without fitting or correction.

## Linear-slot-diffuser.pdf

**alsharqa.linear-slot.supply**

- Airflow is CFM per foot of diffuser, while NC uses a four-foot unit.
- For vertical discharge the source instructs subtracting 5 from NC. Stored rows are the original horizontal-discharge data.

**alsharqa.linear-slot.return**

- Airflow is CFM per foot of diffuser, while NC uses a four-foot unit.
- The static-pressure header has no identified operating-flow row; it is available in a separate table and is not attached to every NC operating point.

**alsharqa.linear-slot.return-header-area**

- The source places pressure values under slot-count columns above multiple airflow rows, without assigning a flow. Do not treat the pressure header as a performance curve or pair it with arbitrary airflow.
- The 1-inch effective-area series is smaller than the 3/4-inch series as printed; no cross-size correction is inferred.

## Motorized-Fire-Smoke-Damper.pdf

**alsharqa.sfsd-series.leakage-ratings**

- These separately listed ratings must not be combined into an assumed certified configuration. The database does not verify listing, installation approval or suitability.

**alsharqa.sfsd-series.fire-resistance**

- These separately listed ratings must not be combined into an assumed certified configuration. The database does not verify listing, installation approval or suitability.

**alsharqa.sfsd-series.closure-velocity**

- These separately listed ratings must not be combined into an assumed certified configuration. The database does not verify listing, installation approval or suitability.

**alsharqa.sfsd-series.closed-pressure**

- These separately listed ratings must not be combined into an assumed certified configuration. The database does not verify listing, installation approval or suitability.

**alsharqa.sfsd-series.trip-device**

- Published Fahrenheit/Celsius labels are retained, not treated as exact conversions. Factory installation and wiring with a qualified actuator are required by the source.
- P.3 typical wiring indicates 24 VAC or 230 VAC; p.5 names Belimo FSLF, FSNF, BF and Honeywell MS4620F1203. The PDF does not give model-specific electrical/torque ratings.

**alsharqa.sfsd30.dimensions**

- Published width/height columns are a schedule, not confirmation of every orderable combination. Blank cells remain not supplied.
- Dimensions and construction are manufacturer-published data; this table does not verify certification or fire suitability.

**alsharqa.fsd60.dimensions**

- Published width/height columns are a schedule, not confirmation of every orderable combination. Blank cells remain not supplied.
- Dimensions and construction are manufacturer-published data; this table does not verify certification or fire suitability.

**alsharqa.fsd70.dimensions**

- Published width/height columns are a schedule, not confirmation of every orderable combination. Blank cells remain not supplied.
- Dimensions and construction are manufacturer-published data; this table does not verify certification or fire suitability.

**alsharqa.sfsd50.dimensions**

- Blank blade-count cells are not supplied; counts are not extrapolated.

## ROUND-SWIRL-DIFFUSER.pdf

**alsharqa.ascd.performance**

- NC dashes mean less than 15, as explicitly defined on PDF p.7.
- Throw pairs are preserved in printed order. Their terminal velocities are not defined in this catalog; do not assume another product's convention.

## Round-Volume-Damper.pdf

- PDF p.4: Same ACVD diameter schedule as G.S.V.D-Cat.pdf p.9; imported once.

**alsharqa.mrp.flow-dimensions**

- The source labels the optimum air-flow range in Pa, which is dimensionally inconsistent. Its numeric cells are retained as unqualified printed values with no assigned engineering unit; do not interpret them as verified flow or pressure.
- Pressure-drop curve points are not digitized. The 50 Pa statement refers to the worked graph example, not all rows.

## Round-diffusers.pdf

**alsharqa.round-diffuser.dimensions**

- Nominal inch and millimeter labels are the supplier's paired sizes, not exact unit conversions.

**alsharqa.round-diffuser.supply**

- The table explicitly gives velocity pressure in inch W.G.; it does not repeat a unit for total pressure drop. Total-pressure cells remain unit-unspecified rather than silently assuming one.
- Throw pairs remain in printed order; terminal velocities and room attenuation are not defined in this catalog.

**alsharqa.round-diffuser.return**

- The table explicitly gives velocity pressure in inch W.G.; it does not repeat a unit for total pressure drop. Total-pressure cells remain unit-unspecified rather than silently assuming one.
- Throw pairs remain in printed order; terminal velocities and room attenuation are not defined in this catalog.

## Sound-attenuators.pdf

**alsharqa.rectangular-silencer.insertion-loss**

- The source's positive/negative velocity signs are preserved; it does not define their relation to sound propagation.
- Zero-velocity pressure is a dash, retained as not supplied rather than zero.
- Pressure values on p.5 disagree with the separate p.6 pressure schedule at common velocities. Both tables retain their own source context; no preferred pressure curve is inferred.

**alsharqa.rectangular-silencer.generated-sound**

- The source does not state a reference power or associate this sound-power table with a specific silencer length. Do not equate these values with room NC or sound pressure.

**alsharqa.rectangular-silencer.pressure-schedule**

- This p.6 schedule conflicts with pressure values attached to p.5 insertion-loss data. They remain separate; resolve the applicable design with the supplier.

**alsharqa.rectangular-silencer.airflow**

- Published rounding is retained. This table specifies face dimensions without a particular silencer length.

**alsharqa.rectangular-silencer.elbow-factors**

- Direct connection is explicitly not advised for the first elbow group. No numeric factor is supplied for it.
- Factors multiply laboratory-tested silencer pressure drop and exclude transition, elbow, dump and other component losses.

**alsharqa.rectangular-silencer.fan-spacing**

- Outlet minimum spacing is one equivalent diameter for every 1000 fpm duct velocity. The separate fan sketch on p.8 specifies one fan diameter per 1000 fpm exit velocity; these contexts are not interchangeable.

## VOLUM-DAMPER-_PRESSURE-DROP.pdf

- PDF p.4: Unlabeled numeric matrix: no reliable quantity/unit definition or connection to the adjacent curves. Not exposed as area or correction factors.

**alsharqa.vcd-airfoil.dimensions**

- Drive-arm X values apply to the source's merged row groups.
- The text specifies 120 mm case depth but the adjacent section drawing labels 180 mm overall. These dimensions are not treated as interchangeable.

## ceiling-diffusers.pdf

**alsharqa.scd.supply**

- NC is the room noise criterion based on an 8 dB room effect; bounds are preserved.
- Throw values apply to the four-way pattern. Published rounding of side airflow is retained.

**alsharqa.scd.return**

- NC is the room noise criterion based on an 8 dB room effect; bounds are preserved.
- Return interpretation uses p.20 notes; its pressure symbol says s while table heading says R.

**alsharqa.scd.supply_patterns**

- Original four-way 6x6, 9x9 and 12x12 records remain in alsharqa.scd.supply; this table contains the other patterns/sizes.
- A/B are the directions in the published pattern diagram; a leading dash in a 1/2-way SCFM cell marks absent A, not negative airflow. A is not applicable there.
- Published area, total/side airflow and throw pairs contain inconsistencies, including reversed throw pairs and non-monotonic series. Values are literal, not recalculated or corrected; do not infer physical consistency.
- Examples: p.12 6x15 area 0.25 ft2; p.13 9x15 and p.14 9x18 area 0.25; p.16 12x24 area 0.25. These conflict with nominal dimensions and some return-table areas.
- P.12 6x18 at 250 fpm: 3-way throw prints -94 and 2-way side airflow prints 13-18; these misplaced cells are unknown, not usable throws/airflow.
- P.14 middle block labels 6x21 on the left and 9x21 on the right; width is unknown and that block has a separate ambiguous variant. Its first total flow prints 63 cfm.
- P.18 21x24 one-way at 700 fpm prints side airflow 2800 versus total 2452. Source inconsistencies require manufacturer clarification before selection.

**alsharqa.scd.return_sizes**

- Original 6x6, 9x9 and 12x12 rows remain in alsharqa.scd.return, without duplication.
- P.19 prints 8x18 for the 2.25 ft2 series, not 18x18. The literal size is retained as a separate variant; it conflicts with area/flow and needs manufacturer clarification.
- Supply and return table areas/flows can disagree. Each table retains its own published values. Interpretation notes are on p.20.

**alsharqa.scdp.supply**

- Units and NC interpretation are given on p.24. Pp.22/23 print pressure 0.94 inH2O at 600 fpm between 0.066 and 0.13; retained as printed, not corrected to 0.094.
- P.22 prints 9x9 area 0.5 ft2, while return p.24 prints 0.56. Each table retains its own value.
- 6x6 one-way at 250 fpm prints a single throw value 2 ft. Assignment to the two terminal velocities is ambiguous; both endpoints are unknown.

**alsharqa.scdp.construction**

- Removable aluminum perforated face; extruded aluminum body. Supply may have an opposed-blade damper; return is normally supplied without one.

## disc-valve.pdf

**alsharqa.sdv.dimensions**

- The dimensional table does not print a unit. Numeric dimensions are preserved without assigning an unverified unit; refer to the supplier before fabrication.

**alsharqa.sdv.supply**

- Blank source cells remain not supplied; they do not establish performance at that flow.
- NC is retained as a criterion value, although the source labels it dB.
- Two suspect pressure cells are withheld as unknown: 125 mm/+10/40 cfm prints 30.6; 200 mm/+10/60 cfm prints 16.3. Both reverse the surrounding pressure trend. No decimal correction is inferred.

**alsharqa.sdv.return**

- Blank source cells remain not supplied; they do not establish performance at that flow.
- NC is retained as a criterion value, although the source labels it dB.

## Ball-jet-Diffuser.pdf

**alsharqa.abjd.performance**

- The source does not define the unit or terminal velocities of the three throw values, nor the Ak unit. Do not assume units from another catalog.
- Several 16-inch throw triples are non-monotonic; they are preserved in printed order without repair.
- The source calls NC decibels, but NC is retained as a criterion value, not sound pressure level.

## Drum-Diffuser.pdf

**alsharqa.sdl.performance**

- Two size alternatives share each source column. They are retained as one published group, not merged into an invented size.
- The 1750x300 / 1250x375 group's 1 m/s airflow is printed as 1363 cfm; the non-proportional progression is preserved, not recalculated.

## Flow-Bar-Diffuser.pdf

**alsharqa.sfb-ht.performance**

- Airflow is per meter of length; NC and throw are for a 1200 mm active section.
- Published length factors for throw: 600 mm 0.72; 3000 mm 1.7; 3600 mm 1.8. No calculated rows are stored.
- For divided flow, use the airflow apportioned to each direction.

**alsharqa.sfb-ht.dimensions**

- The third size is called 50 in the model heading, B column and performance table, but 51 mm in the dimensional row label. The discrepancy is unresolved; dimensions are transcribed as printed.

**alsharqa.sfb-jt.performance**

- Airflow is per meter of length; NC and throw are for a 1200 mm active section.
- Published length factors for throw: 600 mm 0.72; 3000 mm 1.7; 3600 mm 1.8. No calculated rows are stored.
- For divided flow, use the airflow apportioned to each direction.
- The source instructs adding 3 NC when a supply unit is used as a return; these rows remain unadjusted supply values.

**alsharqa.sfb-jt.dimensions**

- The third size is called 50 in the model heading, B column and performance table, but 51 mm in the dimensional row label. The discrepancy is unresolved; dimensions are transcribed as printed.

## NON-RETURN-DAMPER.pdf

**alsharqa.kul.technical-data**

- The exhaust differential-pressure cell repeats 396–23256 m3/h at 2.5 m/s. It is withheld as unknown pressure; the repeated flow range is not converted into a pressure.

