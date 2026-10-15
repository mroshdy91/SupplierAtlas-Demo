"""Supply grilles, PDF pp.10–13. Page 12 duplicates page 11 and is not re-imported."""


def nums(text):
    return [v if v.startswith("<") else float(v) for v in text.split()]


def add_grilles(b):
    file="Grilles-_-registers.pdf"
    model=b.model("supply-grille","Supply grille / register","supply grille and register","air_outlets.grilles",file,11)
    sizes=[]
    for height,ranges in [
        (6,[(100,300),(150,350),(200,400),(200,450),(225,525),(300,700),(350,900)]),
        (8,[(150,400),(175,500),(200,550),(225,625),(250,750),(325,950),(400,1150)]),
        (10,[(150,450),(200,600),(250,700),(275,800),(325,1000),(400,1200),(500,1400)]),
        (12,[(200,550),(250,750),(300,850),(325,925),(400,1150),(500,1400),(600,1700)])]:
        sizes += [[w,height,*limits] for w,limits in zip([12,16,18,20,24,30,36],ranges,strict=True)]
    sizes += [[16,14,300,850],[18,14,350,950],[20,14,400,1050],[24,14,450,1200],
              [30,14,550,1600],[36,14,700,2000],[20,18,500,1400],[24,18,600,1650],
              [30,18,750,2100],[36,18,900,2500],[24,24,800,2300],[30,24,1000,2800],[36,24,1200,3200]]
    b.table(model,"size-flow-range","Published available sizes and airflow ranges",
        [("width","in"),("height","in"),("airflow_min","cfm"),("airflow_max","cfm")],sizes,file,10,printed="10",
        row_key=["width","height"],variant_columns=["width","height"],
        notes=["These are the supplier's overview ranges, not verified duty points or suitability limits. Some detailed performance rows fall outside them."])
    # size group, Ak, flows, NC, throws for 0 / 22.5 / 45 degree deflection.
    groups=[
        ["16x12 / 20x10 / 24x8",1,"278 417 556 694 833 972 1111","<20 <20 <20 <20 20 26 32",
         "19 24 32 39 45 49 54","14 20 27 32 37 43 45","12 17 23 26 30 34 37"],
        ["16x14 / 18x12 / 36x6",1.14,"300 450 600 750 900 1050 1200","<20 <20 <20 <20 23 28 33",
         "19 24 32 39 46 51 55","14 20 27 32 37 43 45","12 17 23 26 30 34 37"],
        ["18x14 / 20x12 / 24x10 / 30x8",1.18,"333 500 667 833 1000 1167 1333","<20 <20 20 23 28 33 38",
         "21 26 34 41 48 53 56","15 21 28 33 34 44 45","13 18 23 27 31 34 37"],
        ["20x14 / 24x12 / 36x8",1.41,"400 600 800 1000 1200 1400 1600","<20 <20 23 28 33 38 43",
         "20 28 38 47 54 59 62","14 23 32 38 42 50 51","12 19 27 33 38 42 44"],
        ["30x10",1.41,"417 625 833 1042 1250 1458 1667","<20 <20 23 28 33 38 43",
         "20 28 38 47 54 59 62","14 23 32 38 42 50 51","12 19 27 33 38 42 44"],
        ["24x14",1.65,"467 700 933 1167 1400 1633 1867","<20 <20 23 28 34 39 44",
         "21 30 38 48 54 59 61","14 25 32 38 43 49 51","12 21 26 33 38 41 43"],
        ["20x18 / 30x12 / 36x10",1.80,"600 750 1000 1250 1500 1750 2000","<20 <20 23 28 34 39 44",
         "23 33 41 49 58 64 66","15 28 33 40 46 53 56","13 23 27 33 39 44 46"],
        ["24x18 / 30x14 / 36x12",2.18,"600 900 1200 1500 1800 2100 2400","<20 <20 24 29 34 39 44",
         "26 36 44 51 59 65 68","17 30 37 43 46 53 56","15 25 31 34 39 44 46"],
        ["36x14",2.5,"700 1050 1400 1750 2100 2450 2800","<20 <20 24 29 35 40 45",
         "30 40 49 56 64 69 71","24 33 41 47 50 56 58","21 28 35 38 43 47 48"],
        ["30x18",2.55,"750 1125 1500 1875 2250 2625 3000","<20 <20 24 29 35 40 45",
         "30 40 50 57 65 70 72","24 33 41 47 50 56 58","21 28 35 38 43 47 48"],
        ["24x24",2.6,"800 1200 1600 2000 2400 2800 3200","<20 <20 24 29 35 40 45",
         "31 41 51 38 66 71 73","25 34 42 48 51 57 59","21 28 35 39 44 48 49"],
        ["36x18",2.9,"900 1350 1800 2250 2700 3150 3600","<20 <20 24 29 35 40 45",
         "34 44 55 62 70 74 76","29 38 46 52 55 59 61","24 32 38 42 47 50 51"],
        ["30x24",3.2,"1000 1500 2000 2500 3000 3500 4000","<20 20 25 30 35 41 46",
         "35 45 56 64 72 75 77","29 38 47 53 56 59 61","24 32 38 42 47 50 51"],
        ["36x24",3.9,"1200 1800 2400 3000 3600 4200 4800","<20 21 26 31 36 41 46",
         "40 50 60 70 78 85 90","34 42 50 60 67 74 79","28 35 40 49 56 62 66"]]
    pressure={0:[.0065,.014,.025,.041,.056,.08,.105],22.5:[.0085,.018,.033,.053,.077,.104,.136],
              45:[.0105,.023,.041,.066,.095,.13,.17]}
    rows,pages=[],[]
    for g,(size,ak,q,nc,*throws) in enumerate(groups):
        for angle,throw in zip([0,22.5,45],throws,strict=True):
            for i,(flow,noise,distance) in enumerate(zip(nums(q),nums(nc),nums(throw),strict=True)):
                rows.append([size,ak,200+100*i,angle,flow,pressure[angle][i],noise,distance])
                pages.append(11 if g<7 else 13)
    b.table(model,"performance","Published supply performance by size group and deflection",
        [("size_group_in",None,"string"),("ak","ft2"),("velocity","fpm"),("deflection","deg"),
         ("airflow","cfm"),("static_pressure","inH2O"),("nc","NC"),("throw","ft")],rows,file,11,row_pages=pages,
        row_key=["size_group_in","velocity","deflection"],variant_columns=["size_group_in"],
        context={"mode":"supply","throw_terminal_velocity_status":"not supplied","nc_room_attenuation_status":"not supplied",
                 "nc_angle_specificity":"one NC series is published for each size/flow, not separate angle series"},
        notes=["PDF p.12 repeats p.11; imported once. Each listed size group shares the published performance series.",
               "The 24x24 group at 500 fpm and 0 degrees prints throw 38 ft, between 51 and 66 ft. That non-monotonic source value is retained without correction.",
               "Ak, airflow and velocity do not always satisfy a consistent conversion in the source. They are transcribed independently; no recalculated values replace them."])
