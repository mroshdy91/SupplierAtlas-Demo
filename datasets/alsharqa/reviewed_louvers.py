"""Louver pressure and area matrices, PDF pp.10 and 13; source signs retained."""


def add_louvers(b):
    file="Air-louvers.pdf"
    model=b.model("air-louver","Air louver","fresh/exhaust air louver","air_outlets.louvers",file,4)
    velocities=[1.25,1.5,2,2.5,3,3.5,3.75,4,4.5]
    exhaust=[.248,.331,.564,.814,1.151,1.595,1.825,2.143,3.29]
    intake=[-.35,-.57,-.83,-1.21,-1.69,-2.35,-2.69,-3.27,-3.85]
    b.table(model,"pressure","Published face-velocity pressure data",
        [("face_velocity","m/s"),("exhaust_pressure","mmH2O"),("intake_pressure","mmH2O")],
        list(zip(velocities,exhaust,intake)),file,10,printed="10",variant_columns=[],
        context={"damper_position":"fully open","intake_includes_filter_pressure":True},
        notes=["Negative intake pressures are the source sign convention, not corrected to positive losses.",
               "The source does not identify the filter thickness used for this pressure table; do not assume all filter options have identical losses."])
    sizes=[300,350,400,450,500,550,600,650,700,750,800,850,900,1000]
    matrix=[
        [.038,.049,.055,.063,.069,.077,.084,.091,.098,.105,.111,.119,.125,.139],
        [.049,.057,.065,.073,.082,.089,.097,.106,.114,.122,.13,.138,.147,.163],
        [.055,.065,.074,.084,.093,.102,.111,.121,.13,.14,.148,.158,.167,.186],
        [.063,.073,.084,.094,.105,.115,.125,.136,.146,.156,.167,.178,.188,.209],
        [.069,.082,.093,.105,.116,.128,.139,.152,.163,.175,.186,.198,.209,.23],
        [.077,.089,.102,.115,.128,.14,.153,.166,.179,.191,.204,.218,.23,.256],
        [.084,.097,.111,.125,.139,.153,.167,.181,.195,.209,.223,.237,.251,.279],
        [.091,.106,.121,.136,.152,.166,.181,.196,.212,.227,.242,.257,.272,.302],
        [.098,.114,.13,.146,.163,.179,.195,.212,.228,.244,.26,.277,.293,.325],
        [.105,.122,.14,.156,.175,.191,.209,.227,.244,.261,.279,.296,.314,.349],
        [.11,.13,.148,.167,.186,.204,.223,.242,.26,.279,.297,.316,.335,.372],
        [.119,.138,.158,.178,.197,.217,.237,.257,.277,.296,.316,.335,.356,.395],
        [.125,.147,.167,.188,.209,.23,.251,.272,.293,.314,.335,.356,.376,.418],
        [.139,.163,.186,.21,.23,.256,.279,.302,.325,.349,.372,.395,.418,.464]]
    b.table(model,"effective-area","Effective pressure area",
        [("height","mm"),("width","mm"),("effective_pressure_area","m2")],
        [[h,w,matrix[i][j]] for i,h in enumerate(sizes) for j,w in enumerate(sizes)],file,10,printed="10",
        row_key=["height","width"],variant_columns=["height","width"],
        notes=["The matrix contains small asymmetric values; source rounding and discrepancies are retained. No interpolation is performed."])
    model=b.model("sand-trap-louver","Sand trap louver","sand trap louver","air_outlets.louvers",file,11)
    b.table(model,"pressure","Sand-trap intake pressure requirement",
        [("face_velocity","fpm"),("intake_total_pressure_drop","inH2O")],
        list(zip([100,200,300,400,500,600,700,800],[.022,.071,.174,.31,.45,.59,.72,.86])),
        file,13,printed="13",variant_columns=[])
    sizes=list(range(12,73,6))
    matrix=[
        [.33,.50,.67,.83,1,1.18,1.34,1.51,1.68,1.86,2.03],
        [.50,.76,1,1.27,1.52,1.79,2.04,2.30,2.55,2.81,3.07],
        [.67,1,1.35,1.70,2.05,2.40,2.73,3.08,3.42,3.77,4.12],
        [.83,1.27,1.70,2.13,2.56,3,3.43,3.86,4.29,4.73,5.16],
        [1,1.52,2.05,2.56,3.09,3.60,4.13,4.64,5.17,5.68,6.21],
        [1.09,1.65,2.22,2.78,3.35,3.91,4.47,5.03,5.60,6.16,6.72],
        [1.26,1.91,2.56,3.21,3.86,4.52,5.17,5.82,6.47,7.12,7.77],
        [1.43,2.16,2.91,3.64,4.38,5.11,5.86,6.59,7.33,8.07,8.81],
        [1.60,2.43,3.24,4.07,4.90,5.72,6.55,7.38,8.20,9.03,9.86],
        [1.77,2.68,3.59,4.50,5.42,6.33,7.25,8.16,9.07,9.99,10.90],
        [1.94,2.94,3.94,4.95,5.94,6.94,7.95,8.95,9.94,10.94,11.95]]
    b.table(model,"effective-area","Effective free area (Ak)",
        [("height","in"),("width","in"),("effective_free_area","ft2")],
        [[h,w,matrix[i][j]] for i,h in enumerate(sizes) for j,w in enumerate(sizes)],file,13,printed="13",
        row_key=["height","width"],variant_columns=["height","width"],
        notes=["Height and width are independent axes. The published matrix is asymmetric; dimensions must not be swapped."])
