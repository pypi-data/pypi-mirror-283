from SheetCode import Sheet
import scripts.RT_Common as RT_Common

sheet = Sheet(__file__)

sheet.Name = "Exit Routes"
sheet.Description = ["For each elementary route marked with Referential/Route/@Type='Exit' and in every applicable mode as per <Referential/Route/PossibleModes> (FS, OS or SH),",
                      "a train will be set upstream of the start signal and the route will be set.",
                      "An exit route can be extended to several subsequent signals; each case will be tested as each case is declared as a specific route in the referential" 
                      "We will then check:",
                      "- MA (Length, Release Speed, Danger point, absence of section timers & overlap)",
                      "- Gradient profile",
                      "- Linking",
                      "- SSP for each category",
                      "- Mode profile (depending on mode set)",
                      "Then, train will drive past the start signal and the Level transition will be checked"]

sheet.StartConditions = ["No elementary routes is set or locked.",
                          "No train is set on the track."]

for mode in ["FS", "OS", "SH"]:
    # *********************************************************************************************************************************************
    sheet.Case(f"Route set in {mode}")
    RT_Common.InitialConditionsL2(sheet, RT_Common.Aspects.RNP, RT_Common.InitialPositions.Valid)

    # ---------------------------------------------------------------------------------------------------------------------------------------------
    sheet.Action(f"Set route under test in {mode}")
        
    # Check MA, Gradient, Linking, SSP and MP
    RT_Common.ExpectedResultsRouteCommons(sheet, mode)
    
    sheet.ExpectedResult("SLR: NO level transition annoucement, Packet 41 is not sent by RBC",
                        requirements = ["[L161_ETCS2-TRK_sSyRS_00592]"])
    
    sheet.ExpectedResult("SLR: MA extends outside Level 2 area",
                        requirements = ["[L161_ETCS2-TRK_sSyRS_00589]"])
    
    sheet.ExpectedResult("SLR: Main stopping point connection associated to L1 Signal 3 remains <Object_DYN_CONNECTION/connection/locking_status> = UNLOCKED>",
                        requirements = ["[L161_ETCS2-TRK_sSyRS_00598]"])
    
    # ---------------------------------------------------------------------------------------------------------------------------------------------
    sheet.Action("Drive past the signal")
    if mode == "FS":
        sheet.ExpectedResult("SLR: Position Report with <M_MODE> = 0 (Full supervision)",
                              requirements = ["[L161_ETCS2-TRK_sSyRS_00170]",
                                              "[L161_ETCS2-TRK_sSyRS_00174]",
                                              "[L161_ETCS2-TRK_sSyRS_00268]"])
    if mode == "OS":
        sheet.ExpectedResult("SLR: Position Report with <M_MODE> = 1 (Onsight)",
                              requirements = ["[L161_ETCS2-TRK_sSyRS_00175]"])
    elif mode == "SH":
        sheet.ExpectedResult("SLR: Position Report with <M_MODE> = 3 (Shunting)",
                              requirements = ["[L161_ETCS2-TRK_sSyRS_00171]"])
        
    # ---------------------------------------------------------------------------------------------------------------------------------------------
    sheet.Action("Cross the LTO Balise group")
    sheet.ExpectedResult("SLR: Position Report with <M_LEVEL> = 2 (Level 1)",
                        requirements = ["[L161_ETCS2-TRK_sSyRS_00559]"])
    if mode == "FS":
        sheet.ExpectedResult("SLR: Position Report with <M_MODE> = 0 (Full supervision)")
    if mode == "OS":
        sheet.ExpectedResult("SLR: Position Report with <M_MODE> = 1 (Onsight)")
    elif mode == "SH":
        sheet.ExpectedResult("SLR: Position Report with <M_MODE> = 3 (Shunting)")

    sheet.ExpectedResult("SLR: General message with Packet 42 with <Q_RBC> = 0" ,
                        requirements = ["[L161_ETCS2-TRK_sSyRS_00583]",
                                        "[L161_ETCS2-TRK_sSyRS_00586]"])

    sheet.ExpectedResult("SLR: Message 156: Termination of communication session is received.")

    sheet.ExpectedResult("SLR: Message 39: Acknowledgement of termination of communication is sent.",
                        requirements = ["[L161_ETCS2-TRK_sSyRS_00587]"])


sheet.Save()









