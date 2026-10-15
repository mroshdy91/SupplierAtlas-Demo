"""SJD panel and performance tables, visually reviewed PDF pp.4–5."""


def add_jet(b):
    file="Jet-diffusers.pdf"
    model=b.model("sjd","SJD","jet diffuser","air_outlets.jet_diffusers",file,3)
    single=[[100,200,200,250,250,100],[150,250,250,300,300,150],[200,300,300,350,350,200],
            [250,350,350,400,400,250],[300,400,400,450,450,300],[350,450,450,500,500,350],[400,500,500,550,550,400]]
    b.table(model,"single-panel","Single-jet panel dimensions",
        [("neck_diameter","mm"),("duct_l","mm"),("duct_w","mm"),("a","mm"),("b","mm"),("e","mm")],
        single,file,4,printed="4")
    raw=[
        [100,2,390,200,440,250,200],[100,3,580,200,630,250,200],[100,4,790,200,840,250,200],
        [150,2,490,250,540,300,250],[150,3,730,250,780,300,250],[150,4,990,400,1040,300,250],
        [200,2,590,300,640,350,300],[200,3,880,300,930,350,300],[200,4,1190,300,1240,350,300],
        [250,2,690,400,740,400,350],[250,3,1030,350,1080,400,350],[250,4,1390,350,1440,400,350],
        [300,2,790,400,840,450,400],[300,3,1180,400,1230,450,400],[300,4,1590,400,1640,450,400],
        [350,2,890,450,1040,500,450],[350,3,1330,450,1530,500,450],[350,4,1770,450,1820,500,450],
        [400,2,990,500,1040,550,500],[400,3,1480,500,1530,550,500],[400,4,1970,500,2020,550,500]]
    b.table(model,"multiple-panel","Multiple-jet panel dimensions",
        [("neck_diameter","mm"),("jet_count",None),("duct_l","mm"),("duct_w","mm"),
         ("a","mm"),("b","mm"),("c","mm")],raw,file,4,printed="4",
        row_key=["neck_diameter","jet_count"],variant_columns=["neck_diameter","jet_count"],
        notes=["Values are as printed. SJD150-4P duct width 400, SJD250-2P duct width 400, and SJD350-2P/3P face widths 1040/1530 depart from adjacent patterns. Confirm these dimensions before fabrication; no correction is inferred."])
    groups={
        100:[.0079,[30,40,50,60,70,80,90,110,130],[.0141,.0189,.0236,.0283,.0331,None,.0425,.052,None],
             ["<.25","<.25",1.67,1.81,2.8,3.4,4.3,6.2,8.7],[2.4,2.4,2.7,2.9,3.4,3.7,4,4.3,4.6],
             ["<15","<15","<15",19,24,32,36,40,44]],
        150:[.0177,[60,80,100,120,140,160,200,240,280],[.0283,.0378,.0472,.0567,.066,None,.0945,.113,.132],
             [.51,"<.75",1.4,1.4,1.76,2.13,3.64,5.8,8.5],[2.4,3,3.7,4.6,5,5.5,6.1,6.7,7],
             ["<15","<15","<15",19,24,33,36,40,45]],
        200:[.0314,[110,140,180,210,250,280,350,420,490],[.052,.066,.085,.099,.118,.132,.165,.198,.231],
             ["<.25",.51,.84,1.11,1.71,2.85,3.41,6.1,8.7],[3.7,5.2,5.5,6.1,6.4,7,7.6,8.2,8.5],
             ["<15",18,18,19,24,33,37,40,45]],
        250:[.049,[170,220,280,330,390,440,550,660,770],[.08,.104,.132,.156,.184,.208,.26,.312,.364],
             ["<.25",.51,.84,1.11,1.42,1.76,2.6,3.8,7],[5.5,6.1,6.4,7.3,8.3,8.5,9.5,10.1,10.7],
             ["<15","<15",15,20,25,33,37,42,46]],
        300:[.071,[240,320,400,480,550,630,790,950,1100],[.113,.151,.189,.227,.26,.298,.373,.449,.519],
             ["<.25","<.25",.7,1.11,1.42,2.85,2.56,2.9,5.8],[6.4,7,7.9,8.5,9.5,9.8,11.6,12.2,12.5],
             ["<15","<15","<15",21,27,34,38,43,47]],
        350:[.096,[330,430,540,650,750,860,1070,1290,1500],[.156,.203,.255,.307,.354,.406,.505,.609,.708],
             ["<.25","<.25",.73,1.14,1.14,1.42,1.71,2.9,7.3],[7,7.9,9.5,10.1,11,11.9,12.5,14,15.2],
             ["<15","<15","<15",21,27,36,38,43,47]],
        400:[.126,[420,560,700,840,980,1120,1400,1680,1960],[.198,.264,.331,.397,.463,.529,.66,.793,.926],
             ["<.25","<.25",.84,1.06,.63,.85,1.17,2.05,2.5],[8.2,9.8,11,11.9,12.5,13.1,14.6,16.4,18.3],
             [15,"<15","<15",22,28,36,39,43,47]],
    }
    velocity=[1.5,2,2.5,3,3.5,4,5,6,7]
    vp=[.15,.25,.41,.56,.79,1.016,1.57,2.29,3.1]
    rows=[]
    for size,(area,q,qsi,dp,throw,nc) in groups.items():
        for i in range(9):
            rows.append([size,velocity[i],area,q[i],qsi[i] if qsi[i] is not None else {"status":"unknown"},
                         vp[i],dp[i],throw[i],nc[i]])
    b.table(model,"performance","Single-jet performance",
        [("neck_diameter","mm"),("neck_velocity","m/s"),("neck_area","m2"),("airflow","cfm"),
         ("airflow_si_published","m3/s"),("dynamic_pressure","mmH2O"),("static_pressure","mmH2O"),
         ("throw_0_25m_s","m"),("nc","NC")],rows,file,5,printed="5",
        row_key=["neck_diameter","neck_velocity"],variant_columns=["neck_diameter"],
        context={"room_attenuation_db":10},
        notes=["Three SI airflow cells conflict by about a factor of ten with their CFM cells: 100 mm at 4/7 m/s prints 0.378/0.614 m3/s; 150 mm at 4 m/s prints 0.756. These SI cells are unknown pending clarification; CFM remains as printed.",
               "Non-monotonic static-pressure values at 300 and 400 mm, and the 400 mm NC progression, are preserved as printed. Published rows are not a fitted performance curve."])
