"""Linear-slot tables, visually reviewed pp.10–14. Unassigned pressure header stays separate."""


def matrix(text):
    return [[float(v) if not v.startswith(("<",">")) else v for v in line.split()]
            for line in text.strip().split(";")]


def add_slot(b):
    file="Linear-slot-diffuser.pdf"
    model=b.model("linear-slot","Linear slot diffuser","linear slot diffuser","air_outlets.linear_slot_diffusers",file,4)
    supply_nc={
        .75:matrix("<20 <20 <20 <20 <20 <20 <20 <20; <20 <20 <20 20 22 23 25 27; 20 22 24 26 27 28 29 30; 25 26 28 30 31 32 33 34; 30 32 33 34 35 36 37 38; 33 35 37 38 39 40 41 42; 36 38 40 42 43 44 45 46; 39 42 44 46 47 48 49 50; 42 44 46 48 50 52 54 56"),
        1:matrix("<20 <20 <20 <20 <20 <20 <20 <20; <20 <20 <20 <20 21 22 24 26; <20 21 23 25 26 27 28 30; 24 25 26 28 30 31 32 33; 27 29 30 32 34 35 36 37; 30 32 34 36 38 39 40 41; 33 35 37 39 40 41 43 45; 35 38 40 43 45 46 47 49; 39 41 44 46 48 50 52 54")}
    return_nc={
        .75:matrix("<20 <20 <20 <20 <20 <20 <20 <20; <20 <20 20 21 23 24 26 27; 21 22 24 26 28 29 30 31; 25 27 29 31 32 33 34 35; 31 33 34 35 36 37 38 39; 34 36 38 39 40 41 42 43; 37 39 41 43 44 45 46 47; 40 43 45 47 48 49 50 51; 43 45 47 49 51 53 55 57"),
        1:matrix("<20 <20 <20 <20 <20 <20 <20 20; <20 <20 <20 20 22 23 25 26; <20 22 24 26 27 28 29 30; 24 26 27 29 31 32 33 34; 28 29 31 33 35 36 37 38; 31 33 35 37 39 40 41 42; 34 36 38 40 41 42 44 46; 36 39 41 44 46 47 49 50; 40 42 45 47 49 51 52 55")}
    throws={
        .75:["4-8 7-12 7-14 8-16 9-18 11-20 11-22 12-23",
             "6-10 9-15 11-19 12-21 14-24 15-27 17-29 18-31",
             "8-12 10-19 14-24 16-27 18-30 20-33 22-36 24-38",
             "10-14 13-22 17-26 20-30 22-32 25-36 28-39 30-42",
             "12-17 15-24 20-29 24-33 25-34 29-40 31-42 33-45",
             "13-18 17-26 22-33 25-36 27-38 31-44 33-47 34-49",
             "14-20 19-28 24-35 26-38 29-41 33-47 35-51 36-54",
             "15-22 21-30 26-38 27-40 32-45 35-50 37-54 38-58",
             "17-24 24-33 29-40 28-44 35-50 37-54 39-58 40-62"],
        1:["4-7 7-11 7-13 8-15 9-17 11-19 11-21 12-22",
           "5-9 8-14 10-18 11-20 13-23 14-26 16-27 17-30",
           "8-12 9-19 13-23 15-26 17-29 19-32 21-34 23-36",
           "9-14 12-21 16-25 20-30 21-31 24-36 27-38 29-40",
           "11-17 14-23 18-28 23-32 24-34 27-39 30-40 32-44",
           "12-18 16-25 21-32 24-36 26-38 30-43 32-46 33-48",
           "14-20 18-28 23-34 25-38 28-42 31-46 34-50 36-52",
           "15-22 20-30 25-38 26-40 30-44 34-49 36-52 37-56",
           "16-24 24-32 27-39 29-43 34-49 36-53 38-56 39-60"]}
    for mode,noise in [("supply",supply_nc),("return",return_nc)]:
        rows,pages=[],[]
        for width in [.75,1]:
            page=(11 if mode=="supply" else 13)+(width==1)
            for i,base_flow in enumerate([10,15,20,25,30,35,40,45,50]):
                for j in range(8):
                    # Every product below is explicitly printed in the source matrix.
                    row=[width,j+1,base_flow*(j+1),noise[width][i][j]]
                    if mode=="supply":row += list(map(int,throws[width][i].split()[j].split("-")))
                    rows.append(row)
                    pages.append(page)
        columns=[("slot_width","in"),("slot_count",None),("airflow_per_length","cfm/ft"),("nc","NC")]
        if mode=="supply":columns += [("throw_100fpm","ft"),("throw_50fpm","ft")]
        b.table(model,mode,"Linear-slot " + mode + " performance",columns,rows,file,pages[0],row_pages=pages,
            row_key=["slot_width","slot_count","airflow_per_length"],variant_columns=["slot_width","slot_count"],
            context={"mode":mode,"nc_reference_length_ft":4,"room_attenuation_db":10,
                     "discharge":"horizontal" if mode=="supply" else "return with deflection blades"},
            notes=["Airflow is CFM per foot of diffuser, while NC uses a four-foot unit."] +
                  (["For vertical discharge the source instructs subtracting 5 from NC. Stored rows are the original horizontal-discharge data."] if mode=="supply" else
                   ["The static-pressure header has no identified operating-flow row; it is available in a separate table and is not attached to every NC operating point."]))
    rows=[]
    for width,a,bb in [(.75,[45,76,111,147,180,215,250,280],[83,117.5,152,186.5,221,251.5,290,324.5]),
                       (1,[51,88,129,171,210,251,292,328],[89,129.5,170,210.5,251,291,332,372.5])]:
        rows += [[width,i+1,a[i],bb[i]] for i in range(8)]
    b.table(model,"dimensions","Linear-slot cross-section dimensions",
        [("slot_width","in"),("slot_count",None),("a","mm"),("b","mm")],rows,file,10,printed="10",
        row_key=["slot_width","slot_count"],variant_columns=["slot_width","slot_count"],context={"section_height_mm":60})
    rows,pages=[],[]
    for width,pressure,area in [(.75,[.007,.030,.062,.117,.173,.236,.335,.452],[.046,.092,.138,.184,.230,.276,.322,.368]),
                               (1,[.005,.020,.044,.078,.115,.164,.231,.310],[.034,.065,.093,.131,.143,.174,.207,.234])]:
        rows += [[width,i+1,pressure[i],area[i]] for i in range(8)]
        pages += [13+(width==1)]*8
    b.table(model,"return-header-area","Return pressure header and effective free area",
        [("slot_width","in"),("slot_count",None),("static_pressure_header","inH2O"),("effective_free_area_per_length","ft2/ft")],
        rows,file,13,row_pages=pages,row_key=["slot_width","slot_count"],variant_columns=["slot_width","slot_count"],
        context={"area_caption_model":"DLC-CR","pressure_operating_airflow_status":"not supplied"},
        notes=["The source places pressure values under slot-count columns above multiple airflow rows, without assigning a flow. Do not treat the pressure header as a performance curve or pair it with arbitrary airflow.",
               "The 1-inch effective-area series is smaller than the 3/4-inch series as printed; no cross-size correction is inferred."])
