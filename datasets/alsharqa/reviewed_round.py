"""Round-diffuser matrices, PDF pp.5–6, preserved without interpolating points."""


def add_round(b):
    # size: neck area, Ak, CFM, supply total pressure, supply NC, throw pairs,
    # return total pressure and return NC. All columns are in printed order.
    groups = {
        6: [.196,.13,[60,80,100,120,135,155,195,235,275,315],
            [.025,.041,.061,.082,.106,.132,.201,.282,.380,.480],
            ["<20","<20","<20","<20","<20",25,30,35,39,45],
            "3-5 3-6 3-6 4-6 4-6 4-6 5-7 5-7 6-8 7-10",
            [.029,.048,.076,.108,.146,.188,.294,.421,.569,.749],
            ["<20","<20","<20","<20",21,26,32,37,41,46]],
        8: [.349,.22,[105,140,175,210,245,280,350,420,490,560],
            [.021,.032,.052,.071,.100,.122,.183,.271,.370,.480],
            ["<20","<20","<20",20,25,29,33,38,42,46],
            "4-6 4-6 5-7 6-8 6-8 6-8 7-10 7-11 8-13 9-14",
            [.020,.034,.053,.077,.100,.123,.207,.293,.394,.519],
            ["<20","<20","<20",21,26,30,34,39,43,47]],
        10: [.545,.25,[165,220,275,325,380,435,545,655,765,870],
             [.040,.061,.092,.122,.181,.242,.361,.500,.710,.950],
             ["<20","<20","<20",21,26,30,34,39,43,47],
             "4-6 6-9 7-10 7-10 7-11 8-13 9-14 10-16 12-18 15-22",
             [.019,.033,.050,.071,.096,.120,.196,.281,.379,.477],
             ["<20","<20","<20",22,27,31,36,41,45,48]],
        12: [.785,.38,[225,315,395,470,550,630,785,940,1100,1255],
             [.026,.041,.072,.101,.152,.201,.313,.490,.670,.870],
             ["<20","<20","<20",22,28,32,36,41,45,48],
             "6-8 7-10 7-11 7-11 8-13 9-14 10-16 14-21 15-23 19-27",
             [.018,.029,.045,.064,.086,.112,.176,.249,.339,.443],
             ["<20","<20","<20",23,29,33,37,42,46,49]],
        14: [1.07,.50,[320,430,535,640,750,855,1070,1285,1500,1710],
             [.034,.051,.080,.112,.156,.201,.313,.460,.600,.800],
             ["<20","<20","<20",24,29,33,37,42,46,49],
             "6-8 8-13 9-15 10-16 11-17 12-18 15-23 19-25 19-27 21-31",
             [.017,.028,.042,.061,.083,.108,.170,.242,.328,.430],
             ["<20","<20",20,25,30,34,38,43,47,50]],
        16: [1.40,.59,[420,560,700,840,980,1120,1400,1680,1960,2240],
             [.043,.075,.106,.140,.202,.262,.413,.593,.800,.980],
             ["<20","<20",20,25,30,34,38,43,47,50],
             "7-11 9-14 9-15 11-17 12-18 15-23 16-25 19-27 21-31 25-36",
             [.016,.025,.041,.059,.079,.103,.162,.231,.314,.411],
             ["<20","<20",21,26,31,35,39,44,48,51]],
    }
    velocities=[300,400,500,600,700,800,1000,1200,1400,1600]
    vp=[.007,.011,.016,.023,.031,.041,.064,.091,.123,.161]
    for mode in ["supply","return"]:
        rows,pages=[],[]
        for size,(area,ak,q,sp,snc,throws,rp,rnc) in groups.items():
            for i,throw in enumerate(throws.split()):
                values=[size,velocities[i],area,q[i],vp[i],(sp if mode=="supply" else rp)[i],
                        (snc if mode=="supply" else rnc)[i]]
                if mode=="supply":values += [ak,*map(int,throw.split("-"))]
                rows.append(values)
                pages.append(5 if mode=="supply" and size<16 else 6)
        columns=[("nominal_in","in"),("neck_velocity","fpm"),("neck_area","ft2"),("airflow","cfm"),
                 ("velocity_pressure","inH2O"),("total_pressure_drop_printed",None),("nc","NC")]
        if mode=="supply":columns += [("area_factor","ft2"),("throw_first","ft"),("throw_second","ft")]
        b.table("alsharqa.round-diffuser",mode,"Round diffuser " + mode + " performance",columns,rows,
            "Round-diffusers.pdf",pages[0],row_pages=pages,row_key=["nominal_in","neck_velocity"],variant_columns=["nominal_in"],
            context={"mode":mode,"room_attenuation_status":"not supplied","throw_terminal_velocities_status":"not supplied"},
            notes=["The table explicitly gives velocity pressure in inch W.G.; it does not repeat a unit for total pressure drop. Total-pressure cells remain unit-unspecified rather than silently assuming one.",
                   "Throw pairs remain in printed order; terminal velocities and room attenuation are not defined in this catalog.",
                   "The 12-inch / 300-fpm point prints 225 cfm, which does not equal its published neck area times velocity. The published flow is retained; no corrected operating point is inferred."])
