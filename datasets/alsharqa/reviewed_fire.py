"""SFD technical construction and installation data; manufacturer claims only."""


def add_fire(b):
    file="Fire-Damper-.-.pdf"
    model=b.model("sfd","SFD","curtain fire damper","dampers.fire",file,4)
    b.table(model,"construction","Published SFD construction",
        [("configuration",None,"string"),("frame_thickness","mm"),("blade_thickness","mm"),
         ("blade_ramp_thickness","mm"),("spring_count",None)],
        [["standard",1.6,1,1.6,2]],file,4,printed="3",variant_columns=[],
        context={"frame_material":"galvanized iron sheet","blade_material":"galvanized steel",
                 "spring_material":"stainless steel","spring_type":"constant force"},
        notes=["The text specifies a 1.6 mm frame, while the drawing says 20-gauge GI casing. These descriptions conflict and must not be treated as equivalent."])
    b.table(model,"installation-limits","Published single-section limits and fusible-link options",
        [("orientation",None,"string"),("fusible_link_temperature","degF"),("maximum_width","in"),("maximum_height","in")],
        [["vertical",165,27,41],["vertical",212,27,41],["horizontal",165,36,36]],file,6,printed="5",
        row_key=["orientation","fusible_link_temperature"],variant_columns=["orientation","fusible_link_temperature"],
        context={"link_options_pdf_page":5,"limit_scope":"single section; supplier's stated maximum rated size"},
        notes=["The source pairs vertical 27x41 inches with 672x1026 mm, which is not an exact conversion. Only the printed inch limits are used here; no corrected metric rating is invented.",
               "These are published product limits, not independent confirmation of listing, installation compliance, or suitability."])
    b.table(model,"installation-details","Published sleeve and retaining-angle details",
        [("configuration",None,"string"),("sleeve_thickness_min","mm"),("sleeve_thickness_max","mm"),
         ("retaining_angle_leg","mm"),("retaining_angle_thickness","mm"),("wall_overlap_min","mm"),
         ("fastener_spacing_max","mm"),("fastener_end_distance","mm")],
        [["text instructions",1.6,3.5,38,2,25,150,50]],file,5,printed="4",variant_columns=[],
        context={"sleeve_requirement":"thicker than connected duct","retaining_angles":"both wall sides; attach to sleeve, not each other or wall",
                 "fasteners":"M5 bolts or 5 mm diameter x 20 mm steel rivets"},
        notes=["The text specifies retaining angles 38x38x2 mm, while the diagram shows 40x40x3 mm and 6 mm bolts. This unresolved difference is disclosed rather than merged.",
               "Sleeve projection is 152 mm maximum in text, 150 mm in the diagram.",
               "PDF p.6 specifies opening clearance 1/4 inch larger up to 24-inch dampers, plus 1/8 inch per additional linear foot. Follow the damper airflow arrow and provide inspection access; these are supplier instructions, not a substitute for an approved installation detail."])
