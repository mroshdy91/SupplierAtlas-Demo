"""Published dimensional tables, visually checked against the identified PDF pages.

Apparent source errors are withheld, never silently corrected.
"""


def add_dimensions(b):
    add_fire_smoke(b)
    add_outlet_dimensions(b)
    file = "Access-door.pdf"
    model = b.model("access-door", "Access door", "duct access door", "ductwork.access_doors", file, 4)
    rows = []
    for size in [6, 8, 10, 12, 14, 16, 18, 20, 24]:
        # These fractions are printed repeatedly in the source dimension schedule.
        rows.append([size, size, {"status": "unknown"} if size == 12 else size,
                     size - 1.125, size - 1.125, 1 if size <= 14 else 2])
    b.table(model, "dimensions", "Standard access-door dimensions",
        [("nominal_size", "in"), ("a", "in"), ("b", "in"), ("neck_width", "in"),
         ("neck_height", "in"), ("cam_locks", None)], rows, file, 5, printed="5",
        context={"frame_material": "22 gauge galvanized steel", "insulation_thickness_mm": 25,
                 "insulation_density_options_kg_m3": [24, 48], "technical_context_pdf_page": 4},
        notes=["The 12x12 row prints B=42 inches. B is withheld as unknown pending supplier clarification; no correction to 12 is inferred."])

    file = "G.S.V.D-Cat.pdf"
    model = b.model("afvd", "AFVD", "flanged volume control damper", "dampers.volume_control", file, 2)
    pairs = [(100,100,1),(150,150,1),(200,200,1),(250,250,1),(300,300,2),(350,350,2),
             (400,400,2),(450,450,2),(500,500,3),(550,600,3),(600,700,4),(650,800,5),
             (700,900,5),(750,1000,6),(800,1100,7),(850,1200,7),(900,1300,8),
             (950,1400,8),(1000,1500,9),(1050,1600,10),(1100,1700,11),(1200,1800,12)]
    dims = [("width", "mm"), ("height", "mm"), ("blade_count", None)]
    note = "Rows preserve the published width/height/blade schedule; they do not assert an exhaustive set of orderable width-height combinations."
    b.table(model, "dimensions", "Published standard size schedule", dims, pairs, file, 4,
        printed="3", row_key=["width", "height"], variant_columns=["width", "height"],
        context={"blade_action_standard": "parallel", "blade_action_option": "opposed",
                 "operating_temperature_c": {"min": -40, "max": 100},
                 "temperature_scope": "standard construction", "technical_context_pdf_page": 3},
        notes=[note, "The p.3 narrative says single blade up to 300 mm height, while the p.4 table lists two blades at 300 mm; the table is retained with this conflict disclosed."])
    model = b.model("acvd-multiblade", "ACVD", "circular-spigot multiblade volume control damper", "dampers.volume_control", file, 5)
    pairs = [(100,100,1),(150,150,1),(200,200,1),(250,250,1),(300,300,2),(350,350,2),
             (400,400,2),(450,450,3),(500,500,3),(550,600,4),(600,700,4),(650,800,5),
             (700,900,6),(750,1000,6),(800,1100,7),(850,1150,7)]
    b.table(model, "dimensions", "Visible standard size schedule", dims, pairs, file, 7,
        printed="6", row_key=["width", "height"], variant_columns=["width", "height"],
        context={"case_length_mm": 380, "operating_temperature_c": {"min": -40, "max": 100},
                 "temperature_scope": "standard construction", "technical_context_pdf_page": 6},
        notes=[note, "A blue block obscures the lower part of the published schedule. Hidden cells are not inferred."])
    model = b.model("acvd-round", "ACVD", "round single-blade volume control damper", "dampers.volume_control", file, 8)
    diameters = [80,100,125,140,150,160,180,200,224,250,280,305,315,350,400,450,500,550,600,610]
    b.table(model, "diameters", "Standard nominal diameters", [("diameter", "mm")],
        [[d] for d in diameters], file, 9, printed="8",
        context={"diagram_outside_diameter": "D - 3 mm"},
        notes=["The same diameter schedule is also published in Round Volume Damper PDF p.4; it is imported once."])

    file = "Round-Volume-Damper.pdf"
    model = b.model("mrp", "MRP-1", "round volume regulator dimension and flow schedule", "dampers.volume_control", file, 6)
    raw = [[80,40,125,50,108,120,40],[100,70,200,75,170,170,40],[125,100,280,120,265,170,40],
           [140,140,400,150,330,170,40],[160,180,500,200,430,240,40],[200,250,900,300,670,240,40],
           [250,500,1500,480,1050,240,40],[315,600,2200,770,1900,220,60],[400,1000,3800,1240,2850,295,60]]
    b.table(model, "flow-dimensions", "Published flow and dimensional schedule",
        [("diameter", "mm"), ("allowable_flow_min", "m3/h"), ("allowable_flow_max", "m3/h"),
         ("optimum_min_printed", None), ("optimum_max_printed", None), ("l1", "mm"), ("l2", "mm")],
        raw, file, 6, printed="6", context={"max_static_pressure_drop_pa": 1000,
            "recommended_duct_velocity_m_s": {"min": 2.7, "max": 6.0, "qualifier": "approximately"}},
        notes=["The source labels the optimum air-flow range in Pa, which is dimensionally inconsistent. Its numeric cells are retained as unqualified printed values with no assigned engineering unit; do not interpret them as verified flow or pressure.",
               "Pressure-drop curve points are not digitized. The 50 Pa statement refers to the worked graph example, not all rows."])

    file = "NON-RETURN-DAMPER.pdf"
    model = b.model("kul", "KUL", "non-return damper", "dampers.non_return", file, 2)
    b.table(model, "technical-data", "Published technical limits",
        [("configuration", None, "string"), ("width_min", "mm"), ("height_min", "mm"),
         ("width_max", "mm"), ("height_max", "mm"), ("airflow_min", "L/s"), ("airflow_max", "L/s"),
         ("face_velocity", "m/s"), ("fresh_air_pressure_drop", "Pa"), ("exhaust_air_pressure_drop", "Pa")],
        [["standard",200,215,1600,1615,110,6460,2.5,25,{"status":"unknown"}]], file, 3, printed="2",
        context={"casing_thickness_mm": 1.25, "blade_thickness_mm": 1, "closing_action": "gravity"},
        notes=["The exhaust differential-pressure cell repeats 396–23256 m3/h at 2.5 m/s. It is withheld as unknown pressure; the repeated flow range is not converted into a pressure."])


def add_fire_smoke(b):
    file = "Motorized-Fire-Smoke-Damper.pdf"
    model = b.model("sfsd-series", "SFSD series", "fire smoke damper series published ratings", "dampers.fire_smoke", file, 2)
    claim = {"status":"manufacturer-published claim; certification not independently verified",
             "scope":"SFSD series; source does not map ratings to individual sizes or actuator combinations",
             "ul_file_as_printed":"R22165"}
    note = ["These separately listed ratings must not be combined into an assumed certified configuration. The database does not verify listing, installation approval or suitability."]
    b.table(model,"leakage-ratings","Published leakage class and temperature pairs",
        [("leakage_class",None,"string"),("temperature","degF")],[["I",350],["II",250]],file,2,
        context=claim,notes=note)
    b.table(model,"fire-resistance","Published fire-resistance durations",
        [("duration","h")],[[1.5],[3]],file,2,context=claim,notes=note,variant_columns=[])
    b.table(model,"closure-velocity","Published dynamic-closure velocities",
        [("velocity","fpm")],[[2000],[4000]],file,2,context=claim,notes=note,variant_columns=[])
    b.table(model,"closed-pressure","Published closed-damper pressure rating",
        [("pressure","inH2O")],[[4]],file,2,context=claim,notes=note,variant_columns=[])
    b.table(model,"trip-device","Published thermoelectric trip device",
        [("model",None,"string"),("temperature_f","degF"),("temperature_c","degC")],
        [["BAE165_US",165,74]],file,2,
        notes=["Published Fahrenheit/Celsius labels are retained, not treated as exact conversions. Factory installation and wiring with a qualified actuator are required by the source.",
               "P.3 typical wiring indicates 24 VAC or 230 VAC; p.5 names Belimo FSLF, FSNF, BF and Honeywell MS4620F1203. The PDF does not give model-specific electrical/torque ratings."])
    square = [[200,200,1],[250,250,1],[300,300,2],[350,350,2],[400,400,2],[450,450,3],
              [500,500,3],[550,600,4],[600,700,4],[650,800,5],[700,900,6],[750,1000,6],
              [800,None,None],[850,None,None],[900,None,None],[950,None,None],[1000,None,None]]
    oval = [[250,200,1],[300,250,1],[350,300,2],[400,350,2],[450,400,2],[500,450,2],
            [550,500,3],[600,550,3],[650,600,4],[700,650,4],[750,700,4],[800,750,5],
            [850,800,5],[900,850,5],[950,900,6],[1000,950,6],[1100,1000,6]]
    for key, code, label, page, rows in [
        ("sfsd30", "SFSD 30", "flanged fire smoke damper",7,square),
        ("fsd60", "FSD 60", "oval-spigot fire smoke damper",11,oval),
        ("fsd70", "FSD 70", "rectangular-spigot fire smoke damper",13,square)]:
        model = b.model(key, code, label, "dampers.fire_smoke", file, page-1)
        b.table(model, "dimensions", "Published standard size schedule",
            [("width", "mm"),("height", "mm"),("blade_count",None)], rows, file, page,
            printed=str(page-1), context={"standard_fusible_link_c":74, "frame_thickness_mm":1.25,
                "blade_thickness_mm":1.25, "blade_action":"parallel", "context_pdf_page":page-1},
            notes=["Published width/height columns are a schedule, not confirmation of every orderable combination. Blank cells remain not supplied.",
                   "Dimensions and construction are manufacturer-published data; this table does not verify certification or fire suitability."])
    model = b.model("sfsd50", "SFSD 50", "circular-spigot fire smoke damper", "dampers.fire_smoke", file, 8)
    diameters = list(range(200,1001,50))
    blades = [1,1,2,2,2,2,3,3,4,4,5,6,None,None,None,None,None]
    b.table(model, "dimensions", "Published circular diameter schedule",
        [("diameter","mm"),("blade_count",None)], list(zip(diameters,blades)), file,9,printed="8",
        context={"case_length_mm":530,"standard_fusible_link_c":74},
        notes=["Blank blade-count cells are not supplied; counts are not extrapolated."])
    file = "VOLUM-DAMPER-_PRESSURE-DROP.pdf"
    model = b.model("vcd-airfoil", "VCD", "aluminum airfoil opposed-blade damper", "dampers.volume_control",file,2)
    b.table(model, "dimensions", "VCD blade and drive-arm dimensions",
        [("l","mm"),("w","mm"),("blade_count",None),("drive_arm_x","mm")],
        [[200,204,2,52],[300,304,3,252],[400,404,4,252],[500,504,5,252],[600,604,6,252],
         [700,704,7,252],[800,804,8,452],[900,904,9,452],[1000,1004,10,452]],file,2,printed="1",
        context={"blade_pitch_mm":100,"case_depth_text_mm":120,"gear_temperature_resistance_c":70},
        notes=["Drive-arm X values apply to the source's merged row groups.",
               "The text specifies 120 mm case depth but the adjacent section drawing labels 180 mm overall. These dimensions are not treated as interchangeable."])


def add_outlet_dimensions(b):
    file = "disc-valve.pdf"
    model = b.model("sdv", "SDV", "disc valve", "air_outlets.disc_valves", file,3)
    b.table(model,"dimensions","Disc valve dimensions",
        [("nominal_size",None),("a",None),("b",None),("c",None),("d",None)],
        [[80,115,62,42,77.5],[100,138,75,40,97.5],[125,164,100,46,122.5],
         [160,211,130,54,157.5],[200,248,158,63,197.5],[250,305,215,75,248]],file,4,printed="3",
        notes=["The dimensional table does not print a unit. Numeric dimensions are preserved without assigning an unverified unit; refer to the supplier before fabrication."])
    file = "Round-diffusers.pdf"
    model = b.model("round-diffuser", "SRD / RRD", "round diffuser", "air_outlets.round_diffusers",file,4)
    b.table(model,"dimensions","Round diffuser dimensions",
        [("nominal_in","in"),("nominal_mm","mm"),("d","mm"),("n","mm"),("e","mm")],
        [[6,160,263,223,154],[8,200,303,263,194],[10,250,353,313,244],
         [12,315,418,378,309],[14,355,458,418,349],[16,400,503,463,394]],file,7,printed="7",
        notes=["Nominal inch and millimeter labels are the supplier's paired sizes, not exact unit conversions."])
    file = "ROUND-SWIRL-DIFFUSER.pdf"
    model = b.model("ascd", "ASCD", "round swirl diffuser", "air_outlets.swirl_diffusers",file,5)
    b.table(model,"dimensions","Swirl diffuser and plenum dimensions",
        [(c,"mm") for c in ["nominal_size","b","d","h2","h3","l","d1","d2","t"]],
        [[315,313,315,200,425,435,480,250,63],[400,398,400,215,530,500,565,300,80],
         [500,500,586,235,630,600,700,350,100],[630,630,708,285,750,750,871,400,125],
         [800,800,871,440,1000,1000,1077,500,160]],file,5,printed="4")
