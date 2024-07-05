from SheetCode import Sheet
import scripts.RT_Common as RT_Common

sheet = Sheet(__file__)

sheet.Name = "Emergency Detectors"
sheet.Description =["For each CSTR in <Referential/CSTR> and each route within this CSTR:",
                    "   - a train will be placed upstream of the start signal and the route will be set",
                    "   - train will be moved to the route and go to FS mode",
                    "   - the CSTR will be activated, which will close the start signal",
                    "   - RBC shall send a UES"]


sheet.StartConditions = ["No elementary routes are set and no routes are locked. ",
                        "Elementary route to be tested is not set.",
                        "Train is at standstill in rear of the start signal of the elementary route to be tested in FS mode and shall fit to all possible train categories (i.e. the train belongs to train categories 1 to 15).",
                        "The train simulator  tool is configured to acknowledge manually the OS mode profile."]

for mode in ["FS", "OS", "SH"]:
    # *********************************************************************************************************************************************
    sheet.Case(f"Route set in {mode} to CSTR entrance")
    RT_Common.InitialConditionsL2(sheet, RT_Common.Aspects.RNP, RT_Common.InitialPositions.Valid)

    # ---------------------------------------------------------------------------------------------------------------------------------------------
    sheet.Action(f"Set route under test in {mode}")
    
    sheet.ExpectedResult("SLR: MA is received")
    
    # ---------------------------------------------------------------------------------------------------------------------------------------------
    sheet.Action("Drive past the signal")
    if mode == "FS":
        sheet.ExpectedResult("SLR: Position Report with <M_MODE> = 0 (Full supervision)")
    if mode == "OS":
        sheet.ExpectedResult("SLR: Position Report with <M_MODE> = 1 (Onsight)")
    elif mode == "SH":
        sheet.ExpectedResult("SLR: Position Report with <M_MODE> = 3 (Shunting)")
    
    # ---------------------------------------------------------------------------------------------------------------------------------------------
    sheet.Action(f"Activate CSTR whose this route belongs")
    
    sheet.ExpectedResult("SLR: For each <Referential/CSTRs/CSTR/EmergencyDetectors/EmergencyDetector>, <Object_DYN_EMERGENCY_DETECTOR/emergency_detector/emergency_status> = TRUE",
                    requirements = ["[L161_ETCS2-TRK_sSyRS_00194]",
                                    "[L161_ETCS2-TRK_sSyRS_00197]",
                                    "[L161_ETCS2-TRK_sSyRS_00221]",
                                    "[L161_ETCS2-TRK_sSyRS_00223]"],
                    parameters = ["LK/Output/Emergency Detectors/emergency_status"])
    
    sheet.ExpectedResult("SLR: Unconditional Emergency Stop Message 15 is sent",
                    requirements = ["[L161_ETCS2-TRK_sSyRS_00192]",
                                    "[L161_ETCS2-TRK_sSyRS_00193]",
                                    "[L161_ETCS2-TRK_sSyRS_00723]",
                                    "[L161_ETCS2-TRK_sSyRS_00199]",
                                    "[L161_ETCS2-TRK_sSyRS_00225]",
                                    "[L161_ETCS2-TRK_sSyRS_00226]"],
                    parameters = ["Route_Map/RM_operational_conditions_layer/emergency_detectors/emergency_detector/only_applicable_to_electric_train"])
    
    sheet.ExpectedResult("SLR: Position Report with <M_MODE> = 7 (Trip)")
    
    sheet.ExpectedResult("SLR: Acknowledgement of Emergency Stop Message 147 is received",
                    requirements = ["[L161_ETCS2-TRK_sSyRS_00228]",
                                    "[L161_ETCS2-TRK_sSyRS_00229]"])

    # ---------------------------------------------------------------------------------------------------------------------------------------------
    sheet.Action(f"Acknowledge Trip mode")
    
    sheet.ExpectedResult("SLR: Position Report with <M_MODE> = 8 (Post Trip)")
    
    # ---------------------------------------------------------------------------------------------------------------------------------------------
    sheet.Action(f"Perform Override of SvL/EoA")
    
    sheet.ExpectedResult("SLR: Position Report with <M_MODE> = 2 (Staff Responsible)")
    
    sheet.ExpectedResult("SLR: Unconditional Emergency Stop Message 15 is resent",
                    requirements = ["[L161_ETCS2-TRK_sSyRS_00195]",
                                    "[L161_ETCS2-TRK_sSyRS_00227]",
                                    "[L161_ETCS2-TRK_sSyRS_00230]",
                                    "[L161_ETCS2-TRK_sSyRS_00231]"])
    
    sheet.ExpectedResult("SLR: Position Report with <M_MODE> = 7 (Trip)")
    
    sheet.ExpectedResult("SLR: Acknowledgement of Emergency Stop Message 147 is received")

    # ---------------------------------------------------------------------------------------------------------------------------------------------
    sheet.Action(f"Acknowledge Trip mode")
    
    sheet.ExpectedResult("SLR: Position Report with <M_MODE> = 8 (Post Trip)")
    # ---------------------------------------------------------------------------------------------------------------------------------------------
    sheet.Action(f"Deactivate CSTR whose this route belongs")
    
    sheet.ExpectedResult("SLR: For each <Referential/CSTRs/CSTR/EmergencyDetectors/EmergencyDetector>, <Object_DYN_EMERGENCY_DETECTOR/emergency_detector/emergency_status> = FALSE",
                requirements = ["[L161_ETCS2-TRK_sSyRS_00198]"])
    
    # ---------------------------------------------------------------------------------------------------------------------------------------------
    sheet.Action(f"Perform Override of SvL/EoA")
    
    sheet.ExpectedResult("SLR: Position Report with <M_MODE> = 2 (Staff Responsible)",
                         requirements = ["[L161_ETCS2-TRK_sSyRS_00700]"])
    
    sheet.ExpectedResult("SLR: Revocation of Emergency Stop Message 18 is sent",
                          requirements = ["[L161_ETCS2-TRK_sSyRS_00199]",
                                          "[L161_ETCS2-TRK_sSyRS_00161]",
                                          "[L161_ETCS2-TRK_sSyRS_00234]",
                                          "[L161_ETCS2-TRK_sSyRS_00233]"])
    
    sheet.ExpectedResult("SLR: Acknowledgement Message 146 (for previous revocation) is received",
                    requirements = ["[L161_ETCS2-TRK_sSyRS_00228]",
                                    "[L161_ETCS2-TRK_sSyRS_00229]",
                                    "[L161_ETCS2-TRK_sSyRS_00232]",
                                    "[L161_ETCS2-TRK_sSyRS_00235]"])
    
    if mode == "FS":
        sheet.ExpectedResult("SLR: Position Report with <M_MODE> = 0 (Full supervision)")
    if mode == "OS":
        sheet.ExpectedResult("SLR: Position Report with <M_MODE> = 1 (Onsight)")
    elif mode == "SH":
        sheet.ExpectedResult("SLR: Position Report with <M_MODE> = 3 (Shunting)")

                    
sheet.Save()










