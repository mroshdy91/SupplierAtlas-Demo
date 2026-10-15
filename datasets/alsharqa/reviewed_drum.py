"""SDL shared size-group performance, Drum PDF p.3 / Jet PDF p.7."""


def add_drum(b):
    file="Drum-Diffuser.pdf"
    model=b.model("sdl","SDL","drum louver diffuser","air_outlets.drum_diffusers",file,2)
    # Each column applies to both printed neck-size alternatives. Preserve the group.
    groups=["225x150 / 175x200","750x150 / 550x200","1500x150 / 1100x200",
            "1600x200 / 1250x250","1750x250 / 1500x300","1750x300 / 1250x375"]
    q=[[83,261,475,651,914,1363],[124,390,713,974,1373,1615],[162,523,950,1297,1829,2157],
       [204,651,1188,1625,2285,2693],[247,781,1425,1948,2741,3230],[285,912,1663,2275,3197,3772],
       [333,1040,1900,2598,3658,4308],[380,1173,2138,2921,4114,4850],[413,1302,2375,3249,4570,5387]]
    nc=[["<15"]*6,["<15",15,"<15","<15","<15","<15"],[15,16,15,15,16,17],
        [16,18,20,21,23,25],[18,23,28,30,32,31],[24,30,33,33,35,35],
        [27,35,39,40,40,43],[31,39,43,44,47,48],[36,43,47,48,49,50]]
    dp=[[.45,.275,.20,.175,.125,.1],[1.025,.675,.375,.375,.3,.275],[1.75,1.15,.7,.7,.55,.525],
        [2.8,1.825,1.05,1.05,.85,.8],[4.125,2.7,1.575,1.575,1.25,1.175],
        [5.475,3.625,2.175,2.175,1.7,1.6],[7.475,4.5,2.825,2.825,2.2,2.05],
        [9.8,5.975,3.55,3.55,2.775,2.6],[11.55,7.2,4.425,4.425,3.45,3.225]]
    throws=["1-1.2-1.5 3.9-5.8-8.8 4.6-6.0-10.0 7-9.1-14.3 7.3-9.4-15.2 7.0-10.4-17.9",
            "1.8-2.1-3.7 4.5-6.0-10.0 7.0-9.1-14.3 7.6-9.7-15.8 7.6-10.6-17.9 8.2-10.6-19.2",
            "2.7-3.7-6.0 5.8-7.6-12.1 7.6-9.8-15.8 9.1-11.5-18.2 9.4-12.1-21.3 10.0-13.1-21.9",
            "3.4-4.9-7.3 7-9.1-14.3 8.8-11.9-18.6 10.3-13.1-21.3 12.8-15.8-27.4 13.1-16.7-30.4",
            "4.0-5.8-8.8 7.9-10.9-16.7 10.9-14.0-21 13.4-16.1-24.9 14.3-17.9-30.4 17.3-21.3-37.4",
            "4.9-6.4-9.8 9.4-12.4-18.8 13.1-15.8-24.9 14.6-17.9-27.7 17.0-21.0-36.5 20.1-25.9-43.0",
            "5.4-7.0-10.7 10.0-13.1-20.1 14.3-17.0-27.7 16.4-19.8-30.4 19.8-24.0-41.1 23.1-25.9-48.7",
            "5.8-7.9-11.6 10.7-14.0-21.0 15.2-18.2-29.5 18.5-21.9-33.8 21.3-25.9-43.5 25.9-32.3-53.3",
            "6.0-8.2-11.9 10.9-14.3-21 16.4-19.2-30.4 18.8-22.2-34.1 22.2-24.3-45.7 26.2-33.5-54.8"]
    rows=[]
    for i,line in enumerate(throws):
        for j,throw in enumerate(line.split()):
            rows.append([groups[j],1+i*.5,q[i][j],dp[i][j],nc[i][j],*map(float,throw.split("-"))])
    b.table(model,"performance","Drum louver performance by published size group",
        [("neck_size_group",None,"string"),("neck_velocity","m/s"),("airflow","cfm"),
         ("static_pressure","mmH2O"),("nc","NC"),("throw_0_75m_s","m"),
         ("throw_0_5m_s","m"),("throw_0_25m_s","m")],rows,file,3,printed="2",
        row_key=["neck_size_group","neck_velocity"],variant_columns=["neck_size_group"],
        context={"room_attenuation_db":10,"size_group_dimension_unit_status":"not printed on performance page",
                 "also_published":{"document":"Jet-diffusers.pdf","pdf_page":7}},
        notes=["Two size alternatives share each source column. They are retained as one published group, not merged into an invented size.",
               "The 1750x300 / 1250x375 group's 1 m/s airflow is printed as 1363 cfm; the non-proportional progression is preserved, not recalculated."])
