"""ASCD performance transcribed from PDF pp.6–7, including p.7 notes."""


def add_swirl(b):
    groups = {
        315: [.293,[170,210,255,296,340,380,420],[.032,.052,.072,.100,.128,.160,.200],
              ["<15",16,22,26,31,34,38],"5-9 7-13 9-17 10-20 11-22 13-24 14-26","4-7 5-8 5-9 6-11 6-12 7-13 8-14"],
        400: [.549,[420,530,635,740,850,950,1060],[.032,.052,.076,.104,.136,.172,.212],
              ["<15",16,23,27,31,34,39],"11-22 14-25 17-33 20-40 23-46 25-51 28-56","6-12 7-14 8-16 9-18 10-20 11-22 13-24"],
        500: [.938,[655,750,845,940,1125,1345,1500],[.036,.048,.061,.075,.108,.155,.192],
              ["<15",17,21,25,31,36,40],"12-24 14-27 17-35 20-40 22-43 26-52 28-56","6-13 7-15 8-16 9-18 10-19 11-23 13-24"],
        630: [1.055,[740,850,950,1060,1270,1480,1700],[.032,.044,.056,.068,.096,.128,.168],
              ["<15",15,18,22,28,33,37],"12-23 14-25 17-33 20-40 22-43 25-50 28-56","6-13 7-14 8-16 9-17 9-19 11-22 13-24"],
        800: [1.216,[850,1060,1270,1480,1700,1900,2100],[.032,.052,.072,.100,.128,.164,.196],
              [15,21,27,32,37,41,45],"11-22 14-25 16-31 19-38 22-45 24-50 27-55","6-13 7-14 8-15 9-17 10-19 11-21 13-24"],
    }
    rows,pages=[],[]
    for size,(ak,q,tp,nc,vertical,horizontal) in groups.items():
        for i,(v,h) in enumerate(zip(vertical.split(),horizontal.split(),strict=True)):
            rows.append([size,q[i],ak,tp[i],nc[i],*map(int,v.split("-")),*map(int,h.split("-"))])
            pages.append(7 if size==800 else 6)
    b.table("alsharqa.ascd","performance","ASCD supply performance",
        [("nominal_size","mm"),("airflow","cfm"),("ak","ft2"),("total_pressure","inH2O"),("nc","NC"),
         ("vertical_throw_first","ft"),("vertical_throw_second","ft"),
         ("horizontal_throw_first","ft"),("horizontal_throw_second","ft")],rows,"ROUND-SWIRL-DIFFUSER.pdf",6,
        row_pages=pages,row_key=["nominal_size","airflow"],variant_columns=["nominal_size"],
        context={"room_absorption_db":10,"notes_pdf_page":7,"throw_pair_terminal_velocities_status":"not supplied"},
        notes=["NC dashes mean less than 15, as explicitly defined on PDF p.7.",
               "Throw pairs are preserved in printed order. Their terminal velocities are not defined in this catalog; do not assume another product's convention."])
