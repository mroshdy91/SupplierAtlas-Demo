"""Flow-bar tables, checked against PDF pages 6–8 (printed 5–7)."""


def add_flowbar(b):
    file = "Flow-Bar-Diffuser.pdf"
    # slot opening: published flow per meter, static pressure, NC, three throws.
    datasets = {
        "ht": {
            25: [[36,58,79,101,122,144,165],[7,18,34,55,81,112,148],["<10",16,26,33,39,44,49],
                 [[1.5,2.5,4.3],[2.8,4,5.5],[3.8,4.5,6.5],[4.3,5.3,7.3],[4.5,5.8,8.3],[5.3,6,8.8],[5.5,6.8,9.5]]],
            38: [[43,65,86,108,129,151,173],[8,18,32,51,73,99,129],["<10",14,24,31,37,42,48],
                 [[1.8,3,5],[3,4.3,5.8],[4,5,6.8],[4.3,5.5,7.5],[5,5.8,8.3],[5.3,6.5,8.8],[5.5,6.8,9.8]]],
            50: [[43,72,101,129,158,187,216],[5,14,28,46,68,95,127],["<10",11,22,30,36,41,46],
                 [[1.5,2.8,5],[2.8,4.3,6],[4,5.3,7.3],[5,5.8,8.3],[5.3,6.5,9.3],[5.8,7,10],[6,7.5,10.8]]],
        },
        "jt": {
            25: [[31,62,93,124,155,186,217],[2,7,15,27,42,61,83],["<10","<10",17,24,28,32,36],
                 [[.5,1,2.3],[1.3,2.3,4],[2.3,3,5.8],[2.8,4,6.8],[3.3,5.3,7.3],[4,5.8,8],[4.5,6,8.8]]],
            38: [[46,93,139,186,232,279,325],[2,8,18,31,49,70,95],["<10","<10",13,22,28,34,40],
                 [[.5,1.3,2.3],[1.5,2.3,4.5],[2.3,3.3,6.8],[3,4.5,8],[3.8,5.5,9.3],[4.5,6.8,9.8],[5.3,7.5,10.8]]],
            50: [[54,116,178,240,302,364,426],[1,7,15,28,44,64,88],["<10",18,24,28,32,37,40],
                 [[.3,1,2.3],[1.5,2.5,4.5],[2.5,3.8,7],[3,5,9.3],[4,6,10.3],[5,7.3,11.3],[5.5,8.5,12.3]]],
        },
    }
    for mode, groups in datasets.items():
        page = 6 if mode == "ht" else 7
        model = b.model("sfb-" + mode, "SFB-" + mode.upper(), "flow bar " + ("high throw" if mode == "ht" else "jet throw"),
                        "air_outlets.flow_bar_diffusers", file, page)
        rows = []
        for size, (flow, pressure, nc, throws) in groups.items():
            for i in range(7):
                rows.append([size,flow[i],pressure[i],nc[i],*throws[i]])
        b.table(model,"performance","Published supply performance",
            [("slot_opening","mm"),("airflow_per_length","L/s/m"),("static_pressure","Pa"),("nc","NC"),
             ("throw_0_8m_s","m"),("throw_0_5m_s","m"),("throw_0_3m_s","m")],rows,file,page,
            printed=str(page-1),row_key=["slot_opening","airflow_per_length"],variant_columns=["slot_opening"],
            context={"active_length_mm":1200,"room_absorption_db":10,"air_pattern":"1-way",
                "throw_condition":"isothermal","inlet_duct_velocity_m_s":{"qualifier":"lt","value":4},
                "plenum_effect_included":False},
            notes=["Airflow is per meter of length; NC and throw are for a 1200 mm active section.",
                   "Published length factors for throw: 600 mm 0.72; 3000 mm 1.7; 3600 mm 1.8. No calculated rows are stored.",
                   "For divided flow, use the airflow apportioned to each direction."] +
                  (["The source instructs adding 3 NC when a supply unit is used as a return; these rows remain unadjusted supply values."] if mode == "jt" else []))
        b.table(model,"dimensions","Single-slot cross-section dimensions",
            [("slot_opening","mm"),("a","mm"),("b","mm"),("w","mm"),("h","mm")],
            [[25,25,25,70,46],[38,29,38,95,46],[50,37,50,121,46]],file,8,printed="7",
            notes=["The third size is called 50 in the model heading, B column and performance table, but 51 mm in the dimensional row label. The discrepancy is unresolved; dimensions are transcribed as printed."])
