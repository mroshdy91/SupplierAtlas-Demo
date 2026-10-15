"""Ductwork engineering schedules and concise dimensional facts."""


def add_duct(b):
    file="DUCT-WORK.pdf"
    model=b.model("rectangular-duct","Rectangular ductwork","rectangular ductwork","ductwork.ducts",file,4)
    b.table(model,"construction","Published standard duct constructions",
        [("construction",None,"string"),("standard_length","mm"),("insulation_thickness","mm"),
         ("insulation_density","kg/m3"),("maximum_air_velocity","fpm"),("inner_shell",None,"string")],
        [["single wall TDF",None,{"status":"not_applicable"},{"status":"not_applicable"},None,"single metal wall"],
         ["lined",1200,25,48,5000,"BGT-faced liner"],
         ["double wall acoustic",1200,25,48,None,"perforated galvanized steel"],
         ["double wall thermal",1200,None,None,None,"solid galvanized steel"]],
        file,4,row_pages=[4,5,6,7],
        context={"standard_material":"galvanized steel","acoustic_liner_facing":"black glass tissue (BGT)"},
        notes=["Single-wall material options: galvanized steel, stainless steel, aluminum, painted galvanized steel.",
               "Acoustic double-wall outer options: galvanized, stainless, black steel, aluminum or painted steel; inner perforated options: galvanized or black steel.",
               "Thermal double-wall inner and outer options: galvanized, black steel, aluminum, stainless or painted steel. No standard insulation thickness/density is specified for that construction."])
    b.table(model,"liner-fastening","Lined-duct adhesive and welding-pin spacing",
        [("velocity_min","fpm"),("velocity_max","fpm"),("a",None),("b",None),("c",None),("e",None)],
        [[0,2500,76,305,102,457],[2501,5000,76,152,102,406]],file,5,printed="4",variant_columns=[],
        row_key=["velocity_min","velocity_max"],
        context={"pin_spacing_qualifier":"approximate centers","insulation_guard":"26 gauge","insulation_thickness_mm":25,"insulation_density_kg_m3":48},
        notes=["A/B/C/E refer to the source fastening diagram. Their table does not print a unit; values remain unit-unspecified rather than silently converted."])
    model=b.model("branch-takeoff","Branch connection / takeoff","duct branch connections and takeoffs","ductwork.fittings",file,8)
    b.table(model,"dimensions","Published branch-connection dimensions",
        [("connection",None,"string"),("length","mm"),("length_rule",None,"string"),
         ("diameter_min","mm"),("diameter_max","mm")],
        [["45 degree rectangular",None,"L = W/4, minimum 100 mm",None,None],
         ["90 degree rectangular",100,"fixed",None,None],
         ["round flanged",85,"fixed",None,None],["round conical",118,"fixed",None,None],
         ["round spin-in",85,"fixed",None,None],["round spin-in with damper",150,"fixed",80,315]],
        file,8,row_pages=[8,9,10,11,12,13],
        notes=["The source recommends sealant after installation. Rectangular takeoffs can have a splitter damper and acoustic lining/double walls; round takeoffs can have double walls.",
               "The 80–315 mm diameter interval is a published range, not a list of discrete available sizes. Other round diameter schedules are referenced but not provided in this PDF."])
    model=b.model("duct-hardware","Duct hardware","duct connection hardware","ductwork.accessories",file,2)
    b.table(model,"cleat-section","Published cleat section dimensions",
        [("top_overall","mm"),("top_flat","mm"),("left_height","mm"),
         ("lower_horizontal","mm"),("right_height","mm")],[[20,12,12,14,12]],file,2,printed="1",variant_columns=[],
        notes=["Dimension names describe positions in the source section sketch; no sheet thickness is specified for the cleat."])
    b.table(model,"clamp","SACL-30 clamp dimensions",
        [("model",None,"string"),("width","mm"),("left_height","mm"),("right_height","mm"),
         ("thickness","mm"),("bolt_diameter","mm"),("bolt_length","mm")],
        [["SACL-30",33,19,30,3,8,25]],file,2,printed="1")
    b.table(model,"gasket-tape","ET gasket tape dimensions",
        [("type",None,"string"),("thickness","mm"),("width","mm"),("roll_length","m")],
        [["ET",5,20,10]],file,3,printed="2",
        context={"material":"EPDM/neoprene modified closed-cell foam","adhesive":"acrylic pressure-sensitive"})
    b.table(model,"bolts-nuts","Published bolt and nut sizes",
        [("component",None,"string"),("thread",None,"string"),("length","mm")],
        [["bolt","M10",30],["nut","M10",{"status":"not_applicable"}]],file,3,printed="2",
        context={"material":"galvanized steel","bolt":"hexagonal cap screw, full thread","nut":"hexagonal"})
    b.table(model,"corners","TDC/TDF corner hardware",
        [("type",None,"string"),("sheet_gauge",None),("carriage_bolt_hole","in")],
        [["DW-CORNER TDC/TDF for Cornermatic",16,.375],["DW-TDC/TDF manual insertion",16,.375]],file,2,printed="1",
        context={"material":"galvanized steel","gauge_standard_status":"not supplied"})
    model=b.model("splitter-damper","Splitter damper","duct splitter damper","dampers.splitter",file,14)
    b.table(model,"dimension-rules","Published splitter geometry rules",
        [("configuration",None,"string"),("a_min","mm"),("blade_length_rule",None,"string"),
         ("r1_rule",None,"string"),("r2_rule",None,"string")],
        [["single blade standard / aerofoil option",100,"1.5 * A","0.75 * W3","A + R1"]],file,14,printed="13",
        context={"trunk_division_rules": {
            "A": "((W3 * D3) / ((W2 * D2) + (W3 * D3))) * W1",
            "B": "((W2 * D2) / ((W2 * D2) + (W3 * D3))) * W1"},
            "symbol_reference": "W1 x D1, W2 x D2, W3 x D3 and A/B refer to the source branch sketch, PDF p.14.",
            "calculation_status": "published relationships only; not evaluated"},
        notes=["Symbols refer to the source branch sketch. No calculated dimensions, flow split or pressure-loss coefficients are supplied by this table."])
