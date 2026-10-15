"""SLT engineering tables, PDF pp.6–7; unqualified dashes remain missing."""


def add_troffer(b):
    file="Light-troffer-diffusers.pdf"
    model=b.model("slt","SLT-S / SLT-D","light troffer diffuser","air_outlets.light_troffer_diffusers",file,3)
    single={
        4: [[50,60,70,80,90,100,110,120,140],"1-2-10 2-4-14 2-5-17 3-6-19 4-8-20 4-10-21 5-12-22 6-14-24 8-17-25",
            [None,None,None,23,27,31,34,37,42],
            [.053,.076,.104,.136,.171,.202,.255,.305,.415],
            [.048,.070,.095,.124,.157,.194,.234,.279,.380]],
        3: [[40,50,60,70,80,90,100,110,120],"3-6-13 4-8-15 6-10-16 8-11-18 9-13-19 10-14-20 11-15-21 12-16-22 13-17-23",
            [None,22,27,31,35,39,42,45,48],
            [.063,.102,.142,.192,.252,.317,.394,.476,.564],
            [.061,.094,.136,.183,.240,.303,.376,.455,.538]],
        2: [[30,40,50,60,70,80,90],"2-5-11 4-7-13 6-9-15 7-11-17 8-13-18 10-13-19 11-14-20",
            [None,24,30,36,40,45,48],
            [.056,.099,.157,.225,.307,.401,.507],
            [.055,.097,.152,.219,.298,.389,.493]]}
    rows=[]
    for length,(q,throws,nc,p5,p6) in single.items():
        for neck,pressure in [(5,p5),(6,p6)]:
            for i,throw in enumerate(throws.split()):
                rows.append([length,neck,"oval",q[i],pressure[i],nc[i],*map(int,throw.split("-"))])
    columns=[("fixture_length","ft"),("neck_size","in"),("neck_shape",None,"string"),("airflow","cfm"),
             ("total_pressure_printed",None),("nc","NC"),("throw_first","ft"),("throw_second","ft"),("throw_third","ft")]
    notes=["Throw terminal velocities, total-pressure units and NC room attenuation are not specified on these performance pages.",
           "NC dashes have no defined numeric threshold in this catalog and remain not supplied."]
    b.table(model,"single-side","Single-side light-troffer performance",columns,rows,file,6,printed="6",
        row_key=["fixture_length","neck_size","neck_shape","airflow"],variant_columns=["fixture_length","neck_size","neck_shape"],
        context={"side_configuration":"single","nc_room_attenuation_status":"not supplied"},
        notes=notes+["The p.4 narrative describes round inlets while this performance table labels the neck oval; the performance labels are retained."])
    dual={
        4: [[60,80,100,120,140,160,180,200,220],"0-1-3 1-1-5 1-2-8 1-3-10 2-4-12 2-5-13 3-6-14 4-8-15 4-9-16",[
            (5,"round",[.053,.098,.151,.217,.292,.385,.487,.598,.722],[None,None,20,26,30,34,37,41,44]),
            (6,"round",[.034,.057,.090,.130,.175,.232,.294,.356,.441],[None,None,None,24,29,32,36,39,42]),
            (8,"round",[.024,.043,.068,.097,.133,.173,.219,.271,.327],[None,None,None,20,25,29,32,35,38]),
            (5,"LP oval",[.035,.065,.100,.144,.193,.255,.322,.396,.478],[None,None,22,27,32,36,39,42,45]),
            (6,"LP oval",[.025,.042,.067,.097,.131,.173,.219,.265,.328],[None,None,None,23,28,32,35,38,41])]],
        3: [[50,60,70,80,100,120,140,160,180],"1-2-7 1-3-8 2-4-10 2-5-11 4-7-12 6-9-14 6-10-14 7-11-51 8-12-16",[
            (5,"round",[.036,.051,.071,.092,.144,.204,.281,.367,.460],[None,None,None,22,28,33,37,40,43]),
            (6,"round",[.031,.045,.062,.080,.126,.178,.246,.321,.402],[None,None,None,22,28,33,37,40,43]),
            (5,"LP oval",[.036,.051,.071,.092,.144,.204,.281,.367,.460],[None,None,None,22,28,33,37,40,43]),
            (6,"LP oval",[.031,.045,.062,.080,.126,.178,.246,.321,.402],[None,None,None,22,28,33,37,40,43])]],
        2: [[40,50,60,70,80,90,100,110,120],"1-3-7 2-4-8 3-5-9 3-6-10 4-7-11 5-7-11 5-8-12 6-9-12 7-9-13",[
            (5,"round",[.040,.062,.090,.124,.163,.200,.252,.304,.363],[None,None,None,23,27,31,34,37,40]),
            (6,"round",[.039,.061,.088,.118,.151,.197,.242,.302,.348],[None,None,None,23,27,31,34,37,40]),
            (5,"LP oval",[.031,.050,.072,.100,.129,.164,.199,.240,.287],[None,None,None,21,25,29,32,35,38]),
            (6,"LP oval",[.029,.044,.064,.089,.114,.144,.178,.222,.256],[None,None,None,21,25,29,32,35,38])]]}
    rows=[]
    for length,(q,throws,options) in dual.items():
        for neck,shape,pressure,nc in options:
            for i,throw in enumerate(throws.split()):
                rows.append([length,neck,shape,q[i],pressure[i],nc[i],*map(int,throw.split("-"))])
    b.table(model,"dual-side","Dual-side light-troffer performance",columns,rows,file,7,printed="7",
        row_key=["fixture_length","neck_size","neck_shape","airflow"],variant_columns=["fixture_length","neck_size","neck_shape"],
        context={"side_configuration":"dual","nc_room_attenuation_status":"not supplied"},
        notes=notes+["The 3-foot fixture at 160 cfm prints throw 7-11-51 ft; this anomalous triple is retained as printed, not corrected to 15."])
    q=[20,30,40,50,60,70,80,90,100,110,120,140,160,180,200,220]
    vp={5:[.001,.003,.005,.009,.012,.017,.022,.027,.034,.041,.049,.066,.087,.110,.135,.163],
        6:[None,None,None,.004,.006,.008,.010,.013,.016,.020,.023,.031,.041,.052,.063,.078],
        8:[None,None,None,.001,.002,.002,.003,.004,.005,.006,.007,.010,.013,.017,.021,.025]}
    b.table(model,"velocity-pressure","Published velocity-pressure reference",
        [("neck_size","in"),("airflow","cfm"),("velocity_pressure","inH2O")],
        [[neck,flow,values[i]] for neck,values in vp.items() for i,flow in enumerate(q)],file,6,printed="6",
        row_key=["neck_size","airflow"],variant_columns=["neck_size"],
        notes=["Repeated on p.7; imported once. Dashes remain not supplied. This reference table does not state oval/round shape or fixture length."])
