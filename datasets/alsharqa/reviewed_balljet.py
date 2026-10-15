"""ABJD engineering tables, visually transcribed from PDF pages 4 and 5."""


def add_balljet(b):
    file = "Ball-jet-Diffuser.pdf"
    model = b.model("abjd", "ABJD", "ball jet diffuser", "air_outlets.jet_diffusers",file,3)
    sizes = [150,200,250,315,350,400]
    heights = [225,290,340,410,460,515]
    widths = [[225,290,340,410,460,515],[450,580,680,820,920,1030],
              [675,870,1020,1230,1380,1545],[900,1160,1360,1640,1840,2060]]
    rows = [[n+1,size,widths[n][i],heights[i]] for n in range(4) for i,size in enumerate(sizes)]
    b.table(model,"panel-dimensions","ABJD 1P–4P panel dimensions",
        [("jets_per_panel",None),("neck_diameter","mm"),("face_width","mm"),("face_height","mm")],
        rows,file,4,printed="3",row_key=["jets_per_panel","neck_diameter"],
        variant_columns=["jets_per_panel","neck_diameter"])
    groups = {
        6: [.077,[62,92,123,154,185,216,246,277,308,339],
            [.052,.117,.209,.326,.470,.639,.835,1.057,1.305,1.579],
            ["<15","<15",21,26,31,35,38,41,44,46],
            [[25,16,12],[34,21,16],[40,24,18],[45,27,21],[48,29,22],[52,31,24],[54,33,25],[57,34,26],[59,36,27],[61,37,28]]],
        8: [.122,[98,146,195,244,293,342,390,439,488,537],
            [.021,.046,.082,.129,.185,.252,.329,.416,.514,.622],
            ["<15","<15","<15","<15","<15",20,25,29,32,36],
            [[35,19,11],[44,26,14],[51,30,17],[56,34,19],[60,37,21],[63,39,22],[66,42,24],[69,43,25],[71,45,26],[73,47,27]]],
        10: [.175,[140,210,280,350,420,490,560,630,700,770],
             [.009,.021,.037,.058,.084,.114,.149,.189,.233,.282],
             ["<15","<15","<15","<15","<15","<15",18,23,27,31],
             [[41,21,11],[51,28,14],[58,33,17],[64,37,18],[68,40,21],[71,42,21],[75,45,23],[78,47,24],[80,48,25],[82,51,26]]],
        12: [.236,[189,283,378,472,566,661,755,850,944,1038],
             [.018,.042,.074,.116,.166,.227,.296,.375,.462,.560],
             ["<15","<15","<15","<15","<15","<15",19,24,28,32],
             [[44,22,12],[55,28,15],[62,33,17],[68,36,19],[72,39,21],[76,41,22],[80,43,23],[83,45,24],[85,46,25],[88,48,26]]],
        14: [.301,[241,361,481,601,721,841,961,1081,1201,1321],
             [.027,.062,.075,.1,.124,.152,.174,.2,.223,.247],
             ["<15","<15","<15","<15",20,25,27,31,34,37],
             [[46,24,12],[56,30,16],[64,35,18],[70,38,21],[74,40,22],[77,43,24],[81,46,25],[83,47,26],[86,48,27],[90,50,28]]],
        16: [.375,[300,450,600,750,900,1050,1200,1350,1500,1650],
             [.098,.221,.392,.613,.882,1.201,1.569,1.985,2.451,2.966],
             ["<15","<15",17,25,31,37,41,46,49,">50"],
             [[38,21,17],[54,19,23],[58,24,20],[67,22,24],[68,22,24],[77,24,27],[81,21,23],[84,26,24],[86,24,25],[91,24,26]]],
    }
    rows=[]
    for size,(ak,q,dp,nc,throw) in groups.items():
        rows += [[size,800+400*i,ak,q[i],dp[i],nc[i],*throw[i]] for i in range(10)]
    b.table(model,"performance","Published single-outlet engineering performance",
        [("nominal_size","in"),("neck_velocity","fpm"),("ak_printed",None),("airflow","cfm"),
         ("static_pressure","inH2O"),("nc","NC"),("throw_first",None),("throw_second",None),("throw_third",None)],
        rows,file,5,printed="4",row_key=["nominal_size","neck_velocity"],variant_columns=["nominal_size"],
        context={"throw_unit_status":"not supplied","throw_terminal_velocity_status":"not supplied",
                 "ak_unit_status":"not supplied","room_absorption_status":"not supplied"},
        notes=["The source does not define the unit or terminal velocities of the three throw values, nor the Ak unit. Do not assume units from another catalog.",
               "Several 16-inch throw triples are non-monotonic; they are preserved in printed order without repair.",
               "The source calls NC decibels, but NC is retained as a criterion value, not sound pressure level."])
