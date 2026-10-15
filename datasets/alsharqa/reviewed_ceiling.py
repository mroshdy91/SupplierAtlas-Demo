"""Reviewed ceiling supply/return matrices; preserve source defects explicitly."""
from ceiling_supply_data import GROUPS

FILE = "ceiling-diffusers.pdf"
VELOCITIES = [250, 300, 400, 500, 600, 700, 800]
UNKNOWN = {"status": "unknown"}
NA = {"status": "not_applicable"}


def nums(text):
    return [v if v.startswith(("<", ">")) else float(v) for v in text.split()]


def pair(text):
    if text == "?":
        return [UNKNOWN, UNKNOWN]
    return list(map(float, text.split("-")))


def add_ceiling(b):
    model = "alsharqa.scd"
    next(p for p in b.data["products"] if p["id"] == model)["label"] = "Alsharqa SCD ceiling diffuser"
    rows, pages = [], []
    for page, w, h, area, q, nc, patterns in sorted(GROUPS):
        for pattern, (side, throws) in zip([4, 3, 2, 1], patterns, strict=True):
            if page == 9 and pattern == 4:
                continue  # Preserve the existing 21 stable four-way records, without duplication.
            for i, (flow, noise, sides, distances) in enumerate(zip(nums(q), nums(nc), side.split(), throws.split(), strict=True)):
                if pattern in (4, 3):
                    airflow_sides = [UNKNOWN, UNKNOWN] if sides == "?" else list(map(float, sides.split(",")))
                    if distances == "?":
                        a = z = [UNKNOWN, UNKNOWN]
                    elif "," in distances:
                        a, z = map(pair, distances.split(","))
                    else:
                        a = z = pair(distances)
                else:
                    airflow_sides = [NA, UNKNOWN if sides == "?" else float(sides)]
                    a, z = [NA, NA], pair(distances)
                size = f"{w}x{h}"
                width = w
                if (page, w, h) == (14, 9, 21):
                    size, width = "6x21 left / 9x21 right", UNKNOWN
                rows.append([size, width, h, area, pattern, VELOCITIES[i], flow,
                             [.018,.026,.046,.072,.104,.142,.186][i], noise,
                             *airflow_sides, *a, *z])
                pages.append(page)
    b.table(model, "supply_patterns", "Additional published supply sizes and patterns",
        [("size_label",None,"string"),("neck_width","in"),("neck_height","in"),("neck_area","ft2"),
         ("ways",None),("neck_velocity","fpm"),("airflow","cfm"),("pressure_drop","inH2O"),("nc","NC"),
         ("side_airflow_a","cfm"),("side_airflow_b","cfm"),("throw_a_100fpm","ft"),("throw_a_50fpm","ft"),
         ("throw_b_100fpm","ft"),("throw_b_50fpm","ft")], rows, FILE, 9, row_pages=pages,
        row_key=["size_label","ways","neck_velocity"],variant_columns=["size_label"],
        context={"mode":"supply","room_effect_db":8,"throw_terminal_velocities_fpm":[100,50],
                 "pattern_labels":"SCD is printed for both square and rectangular performance tables"},
        notes=["Original four-way 6x6, 9x9 and 12x12 records remain in alsharqa.scd.supply; this table contains the other patterns/sizes.",
               "A/B are the directions in the published pattern diagram; a leading dash in a 1/2-way SCFM cell marks absent A, not negative airflow. A is not applicable there.",
               "Published area, total/side airflow and throw pairs contain inconsistencies, including reversed throw pairs and non-monotonic series. Values are literal, not recalculated or corrected; do not infer physical consistency.",
               "Examples: p.12 6x15 area 0.25 ft2; p.13 9x15 and p.14 9x18 area 0.25; p.16 12x24 area 0.25. These conflict with nominal dimensions and some return-table areas.",
               "P.12 6x18 at 250 fpm: 3-way throw prints -94 and 2-way side airflow prints 13-18; these misplaced cells are unknown, not usable throws/airflow.",
               "P.14 middle block labels 6x21 on the left and 9x21 on the right; width is unknown and that block has a separate ambiguous variant. Its first total flow prints 63 cfm.",
               "P.18 21x24 one-way at 700 fpm prints side airflow 2800 versus total 2452. Source inconsistencies require manufacturer clarification before selection."])
    # Remaining return rows, independently transcribed (not copied from supply).
    groups = [
        (19,15,15,1.56,"390 469 625 781 938 1095 1250","22 25 31 36 40 47 52"),
        (19,8,18,2.25,"562 675 900 1125 1350 1575 1800","20 28 34 39 44 49 55"),
        (19,21,21,3.06,"765 919 1225 1530 1838 2144 2450","26 29 34 40 46 54 60"),
        (19,24,24,4,"1000 1200 1600 2000 2400 2800 3200","24 29 34 41 47 54 59"),
        (19,6,9,.375,"94 113 150 188 226 262 300","<18 <18 21 25 29 34 38"),
        (19,6,12,.5,"125 150 200 250 300 350 400","<18 20 24 29 33 39 44"),
        (19,6,15,.625,"156 188 250 312 376 438 500","<18 21 27 32 36 41 46"),
        (19,6,18,.75,"188 225 300 375 450 526 600","<18 22 28 33 37 42 48"),
        (19,6,21,.875,"219 262 350 438 524 612 700","20 24 30 35 39 44 49"),
        (19,6,24,1,"251 300 400 501 600 700 800","20 24 31 37 41 45 50"),
        (19,9,12,.75,"188 225 300 375 450 526 600","<18 21 27 32 36 41 47"),
        (19,9,15,.938,"234 281 375 468 562 656 756","<18 22 27 33 37 42 45"),
        (19,9,18,1.125,"281 337 450 562 674 788 900","18 24 30 35 38 44 49"),
        (20,9,21,1.31,"328 394 525 656 788 918 1050","21 25 31 36 41 44 48"),
        (20,9,24,1.5,"375 450 600 750 900 1050 1200","21 26 33 38 44 48 53"),
        (20,12,15,1.25,"312 375 500 624 750 876 1000","20 24 31 36 39 43 48"),
        (20,12,18,1.5,"375 450 600 750 900 1050 1200","22 26 32 36 41 46 51"),
        (20,12,21,1.75,"438 525 700 875 1050 1224 1400","23 27 33 36 42 48 52"),
        (20,12,24,2,"500 600 800 1000 1200 1400 1600","25 29 35 40 43 48 53"),
        (20,15,18,1.875,"469 562 750 938 1125 1312 1500","21 26 32 37 42 46 50"),
        (20,15,21,2.185,"548 655 875 1095 1312 1529 1750","22 26 32 38 43 47 51"),
        (20,15,24,2.5,"628 748 1000 1252 1499 1746 2000","24 28 33 39 44 48 53"),
        (20,18,21,2.625,"655 788 1050 1313 1575 1838 2138","21 27 33 39 44 48 54"),
        (20,18,24,3,"748 901 1200 1500 1800 2100 2400","23 28 34 40 45 49 55"),
        (20,21,24,3.5,"871 1053 1400 1748 2100 2452 2800","24 28 33 38 43 49 54")]
    rows, pages = [], []
    for page,w,h,area,q,nc in groups:
        for i,(flow,noise) in enumerate(zip(nums(q),nums(nc),strict=True)):
            rows.append([w,h,area,VELOCITIES[i],flow,[.021,.031,.055,.086,.125,.170,.220][i],noise])
            pages.append(page)
    b.table(model,"return_sizes","Additional published return sizes",
        [("neck_width","in"),("neck_height","in"),("neck_area","ft2"),("neck_velocity","fpm"),
         ("airflow","cfm"),("pressure_drop","inH2O"),("nc","NC")],rows,FILE,19,row_pages=pages,
        row_key=["neck_width","neck_height","neck_velocity"],variant_columns=["neck_width","neck_height"],
        context={"mode":"return","room_effect_db":8,"ways_applicability":[1,2,3,4]},
        notes=["Original 6x6, 9x9 and 12x12 rows remain in alsharqa.scd.return, without duplication.",
               "P.19 prints 8x18 for the 2.25 ft2 series, not 18x18. The literal size is retained as a separate variant; it conflicts with area/flow and needs manufacturer clarification.",
               "Supply and return table areas/flows can disagree. Each table retains its own published values. Interpretation notes are on p.20."])
    add_perforated(b)


def add_perforated(b):
    model=b.model("scdp","SCDP","perforated ceiling diffuser","air_outlets.ceiling_diffusers",FILE,21)
    groups=[
        (22,6,.25,"63 75 100 125 150 175 200","<18 20 22 25 29 34 38",[
            "2-4 3-5 4-6 5-7 6-8 7-9 8-10","2-4 3-5 4-6 5-7 6-7 6-8 7-9",
            "2-3 2-4 3-5 4-6 5-6 5-7 6-8","? 2-3 3-4 3-5 4-5 5-6 6-7"]),
        (22,9,.5,"140 169 225 281 338 394 450","<18 20 23 26 31 36 42",[
            "3-5 5-7 7-9 8-11 10-12 11-14 13-16","3-5 4-6 5-8 7-10 9-11 10-12 11-14",
            "2-4 4-5 5-7 6-9 8-10 9-11 10-12","2-3 3-5 4-6 5-7 7-9 8-10 9-11"]),
        (22,12,1,"250 300 400 500 600 700 800","19 22 25 28 34 39 45",[
            "4-6 6-8 8-11 10-14 12-16 14-19 16-22","4-6 5-7 7-10 9-13 11-14 12-17 14-19",
            "3-5 4-6 6-8 8-11 10-13 11-15 12-17","3-4 4-5 5-7 7-9 8-11 10-14 11-15"]),
        (23,15,1.56,"390 469 625 781 938 1095 1250","20 23 27 32 38 44 50",[
            "5-7 8-10 10-13 12-16 15-20 18-23 20-26","5-6 7-9 9-11 11-14 13-18 16-21 18-23",
            "4-5 6-8 8-10 10-12 11-16 14-18 16-20","3-4 5-7 7-9 9-11 10-14 12-16 14-18"])]
    rows,pages=[],[]
    for page,size,area,q,nc,patterns in groups:
        for ways,throws in zip([4,3,2,1],patterns,strict=True):
            for i,(flow,noise,throw) in enumerate(zip(nums(q),nums(nc),throws.split(),strict=True)):
                rows.append([size,area,ways,VELOCITIES[i],flow,[.015,.023,.041,.066,.94,.13,.172][i],noise,*pair(throw)])
                pages.append(page)
    b.table(model,"supply","Perforated supply performance",
        [("square_neck_size","in"),("neck_area","ft2"),("ways",None),("neck_velocity","fpm"),
         ("airflow","cfm"),("pressure_drop","inH2O"),("nc","NC"),("throw_100fpm","ft"),("throw_50fpm","ft")],
        rows,FILE,22,row_pages=pages,row_key=["square_neck_size","ways","neck_velocity"],
        context={"mode":"supply","room_effect_db":8,"throw_terminal_velocities_fpm":[100,50]},
        notes=["Units and NC interpretation are given on p.24. Pp.22/23 print pressure 0.94 inH2O at 600 fpm between 0.066 and 0.13; retained as printed, not corrected to 0.094.",
               "P.22 prints 9x9 area 0.5 ft2, while return p.24 prints 0.56. Each table retains its own value.",
               "6x6 one-way at 250 fpm prints a single throw value 2 ft. Assignment to the two terminal velocities is ambiguous; both endpoints are unknown."])
    rows=[]
    return_nc=["<18 20 23 26 30 36 39","19 21 24 27 32 37 43","20 23 26 30 35 40 47","21 24 29 35 40 46 52"]
    for (_,size,_,q,_,_),area,nc in zip(groups,[.25,.56,1,1.56],return_nc,strict=True):
        for i,(flow,noise) in enumerate(zip(nums(q),nums(nc),strict=True)):
            rows.append([size,area,VELOCITIES[i],flow,[.019,.032,.059,.091,.115,.148,.198][i],noise])
    b.table(model,"return","Perforated return performance",
        [("square_neck_size","in"),("neck_area","ft2"),("neck_velocity","fpm"),
         ("airflow","cfm"),("pressure_drop","inH2O"),("nc","NC")],rows,FILE,24,
        row_key=["square_neck_size","neck_velocity"],context={"mode":"return","room_effect_db":8})
    b.table(model,"construction","Perforated face construction",
        [("hole_diameter","mm"),("hole_pitch","mm"),("open_face_percent","%"),("face_thickness","mm")],
        [[4,6,40,1.5]],FILE,21,variant_columns=[],
        notes=["Removable aluminum perforated face; extruded aluminum body. Supply may have an opposed-blade damper; return is normally supplied without one."])
