"""Sound attenuator engineering tables, visually reviewed PDF pp.5–8."""


def numbers(text):
    return [[float(v) for v in row.split()] for row in text.split(";")]


def add_sound(b):
    file="Sound-attenuators.pdf"
    model=b.model("rectangular-silencer","Rectangular sound attenuator","rectangular sound attenuator","acoustics.sound_attenuators",file,4)
    bands=[63,125,250,500,1000,2000,4000,8000]
    velocity=[-1750,-1500,-1000,-500,0,500,1000,1500,1750]
    pressure={60:[1.28,.95,.42,.11,None,.11,.42,.95,1.28],
              48:[1.12,.82,.36,.095,None,.095,.36,.82,1.12],
              36:[.95,.7,.31,.08,None,.08,.31,.7,.95],
              24:[.85,.61,.27,.07,None,.07,.27,.61,.85]}
    insertion={
        60:numbers("9 14 31 39 39 23 17 17;9 14 30 40 40 26 21 20;8 12 28 38 41 38 34 23;8 12 27 37 45 48 40 24;7 11 26 36 46 48 41 24;6 11 25 35 46 49 43 26;5 10 23 33 44 43 39 25;5 9 22 31 40 32 25 24;4 9 22 31 37 28 21 20"),
        48:numbers("9 12 24 30 36 22 17 17;8 12 24 28 36 25 21 19;8 11 22 28 34 44 29 21;7 10 22 28 34 44 32 21;7 9 21 28 32 44 30 24;6 9 20 28 32 42 32 23;5 8 19 26 30 40 32 22;5 8 18 24 30 31 24 22;4 7 18 24 30 28 20 18"),
        36:numbers("8 9 18 23 31 21 17 16;8 8 17 23 30 24 21 17;7 8 16 22 29 36 24 16;7 7 16 21 29 38 25 17;7 7 15 20 27 37 25 16;6 7 14 19 27 36 26 16;5 7 13 19 26 36 26 17;5 6 13 18 25 31 24 17;4 6 13 18 24 28 20 17"),
        24:numbers("6 6 12 15 18 21 16 14;6 7 12 14 18 21 16 13;7 6 11 14 17 22 16 14;6 5 11 14 17 22 16 14;6 5 10 14 16 22 15 14;5 5 10 14 16 21 16 13;5 5 9 13 15 21 16 13;4 5 9 12 15 21 16 13;4 3 9 12 15 20 16 13")}
    b.table(model,"insertion-loss","Insertion loss with signed face velocity",
        [("length","in"),("face_velocity","fpm"),("static_pressure_drop","inH2O")]+[(f"il_{f}hz","dB") for f in bands],
        [[length,v,pressure[length][i],*insertion[length][i]] for length in [60,48,36,24] for i,v in enumerate(velocity)],
        file,5,printed="5",row_key=["length","face_velocity"],variant_columns=["length"],
        context={"face_velocity_unit_basis":"fpm on adjacent pressure table, PDF p.6","velocity_sign_meaning_status":"not supplied"},
        notes=["The source's positive/negative velocity signs are preserved; it does not define their relation to sound propagation.",
               "Zero-velocity pressure is a dash, retained as not supplied rather than zero.",
               "Pressure values on p.5 disagree with the separate p.6 pressure schedule at common velocities. Both tables retain their own source context; no preferred pressure curve is inferred."])
    power=numbers("75 62 54 54 57 67 66 60;71 58 49 51 55 65 61 55;63 49 42 45 53 54 48 39;60 47 34 37 36 26 21 25;63 50 35 36 34 25 22 27;64 51 43 45 47 48 43 35;71 62 53 52 55 58 58 52;75 62 57 56 57 62 62 57")
    b.table(model,"generated-sound","Airflow-generated sound power levels",
        [("face_velocity","fpm")]+[(f"lw_{f}hz","dB") for f in bands],
        [[v,*row] for v,row in zip([-1750,-1500,-1000,-500,500,1000,1500,1750],power,strict=True)],
        file,5,printed="5",variant_columns=[],
        context={"reference_power_status":"not supplied","reference_silencer_length_status":"not supplied"},
        notes=["The source does not state a reference power or associate this sound-power table with a specific silencer length. Do not equate these values with room NC or sound pressure."])
    velocities=[500,750,1000,1250,1500,1750,2000]
    dp={60:[.065,.166,.247,.331,.450,.665,.950],48:[.053,.128,.211,.303,.423,.592,.825],
        36:[.042,.099,.175,.275,.395,.520,.700],24:[.025,.064,.110,.209,.330,.447,.610]}
    b.table(model,"pressure-schedule","Separate static pressure-loss schedule (p.6)",
        [("length","in"),("face_velocity","fpm"),("static_pressure_loss","inH2O")],
        [[length,v,values[i]] for length,values in dp.items() for i,v in enumerate(velocities)],file,6,printed="6",
        row_key=["length","face_velocity"],variant_columns=["length"],
        notes=["This p.6 schedule conflicts with pressure values attached to p.5 insertion-loss data. They remain separate; resolve the applicable design with the supplier."])
    airflow=[
        [14,12,1.17,583,875,1167,1458,1750,2042,2333],
        [14,14,1.36,681,1021,1361,1701,2042,2382,2722],
        [28,12,2.33,1167,1750,2333,2917,3500,4083,4667],
        [28,18,3.5,1750,2625,3500,4375,5250,6125,7000],
        [28,20,3.89,1944,2917,3889,4861,5833,6806,7778],
        [28,28,5.44,2722,4083,5444,6806,8167,9528,10889],
        [42,12,3.5,1750,2625,3500,4375,5250,6125,7000],
        [42,18,5.25,2625,3938,5250,6563,7875,9188,10500],
        [42,24,7,3500,5250,7000,8750,10500,12250,14000],
        [42,30,8.75,4375,6563,8750,10938,13125,15313,17500],
        [42,36,10.5,5250,7875,10500,13125,15750,18375,21000],
        [56,18,7,3500,5250,7000,8750,10500,12250,14000],
        [56,27,10.5,5250,7875,10500,13125,15750,18375,21000],
        [56,32,12.44,6222,9333,12444,15556,18667,21778,24889],
        [56,36,14,7000,10500,14000,17500,21000,24500,28000],
        [56,45,17.5,8750,13125,17500,21875,26250,30625,35000],
        [56,54,21,10500,15750,21000,26250,31500,36750,42000],
        [56,60,23.33,11667,17500,23333,29167,35000,40833,46667]]
    b.table(model,"airflow","Published face area and airflow schedule",
        [("width","in"),("height","in"),("face_area","ft2"),("face_velocity","fpm"),("airflow","cfm")],
        [[*row[:3],v,row[3+i]] for row in airflow for i,v in enumerate(velocities)],file,6,printed="6",
        row_key=["width","height","face_velocity"],variant_columns=["width","height"],
        notes=["Published rounding is retained. This table specifies face dimensions without a particular silencer length."])
    elbow=[]
    for configuration,distances,factors in [
        ("radius elbows and square elbows with turning vanes",[3,2,1,.5],[1,1.25,1.75,3]),
        ("radius elbows without turning vanes",[3,2,1],[1,1.25,1.75])]:
        elbow += [[configuration,d,f] for d,f in zip(distances,factors,strict=True)]
    b.table(model,"elbow-factors","Published elbow installation pressure factors",
        [("elbow_configuration",None,"string"),("lu_ld_over_deq",None),("pressure_factor",None)],elbow,file,7,printed="7",
        row_key=["elbow_configuration","lu_ld_over_deq"],variant_columns=[],
        context={"baffle_orientation":"parallel to elbow plane","deq_definition":"circular: duct diameter; rectangular/square: sqrt(4*area/pi)",
                 "notes_pdf_page":8},
        notes=["Direct connection is explicitly not advised for the first elbow group. No numeric factor is supplied for it.",
               "Factors multiply laboratory-tested silencer pressure drop and exclude transition, elbow, dump and other component losses."])
    b.table(model,"fan-spacing","Published vane-axial fan spacing",
        [("arrangement",None,"string"),("inlet_min_over_deq",None),("outlet_min_over_deq_per_1000fpm",None),("pressure_factor",None)],
        [["rectangular silencer / vane axial fan",.75,1,1]],file,7,printed="7",variant_columns=[],
        context={"inlet_transition_angle_deg":30,"outlet_transition_angle_deg":15},
        notes=["Outlet minimum spacing is one equivalent diameter for every 1000 fpm duct velocity. The separate fan sketch on p.8 specifies one fan diameter per 1000 fpm exit velocity; these contexts are not interchangeable."])
