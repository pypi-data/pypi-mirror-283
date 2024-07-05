from SheetCode import Sheet
import scripts.RT_Common as RT_Common
import libs.Referential as Referential

sheet = Sheet(__file__)

sheet.Name = "Conditional Emergency Stop due to EBP's SDG or CLOSE command"
sheet.Description = ["For each elementary route marked with Referential/Route/@Type='Inside' and in every applicable mode as per <Referential/Route/PossibleModes> (FS, OS or SH).",
                      "1) a train is placed upstream of the start signal and the route is set in each mode. We are not checking the MA content as it's done already in RT_* tests",
                      "2) The track downstream is occupied We check that:",
                      "   - CES is sent. The stopping point and revocation of CES are not checked as it's done in CES_REPLACEMENT test.",
                      "Note: SDG applies for Controlled Main Stop signals, and CLOSE applies for Non-Controlled Main Stop Signals and Controlled Automatic Signals"]

sheet.StartConditions = ["No elementary routes is set or locked.",
                          "No train is set on the track."]

routes = Referential.Values(f".//Route/Type[text() = 'Inside']/../@Name")
for route in routes:
    for mode in ["FS", "OS", "SH"]:
        if Referential.Node(f".//Route[@Name = '{route}']/PossibleModes/@{mode}") == True:   
            sheet.StartLoop(f"{route}_{mode}")

            # *********************************************************************************************************************************************
            sheet.Case(f"Route set in {mode}")
            
            RT_Common.InitialConditionsL2(sheet, RT_Common.Aspects.RNP, RT_Common.InitialPositions.Valid)

            # ---------------------------------------------------------------------------------------------------------------------------------------------
            sheet.Action(f"Set route under test in {mode}")
            sheet.ExpectedResult("SLR: MA is sent")
            
            # ---------------------------------------------------------------------------------------------------------------------------------------------
            if mode == "SH":
                sheet.Action(f"Perform a SDG command on the start signal")
            else:
                sheet.Action(f"Perform a CLOSE command on the start signal")
            
            sheet.ExpectedResult("SLR: SLR: For each <Referential/Route/Connections/Connection>, <Object_DYN_CONNECTION/connection/locking_status> = UNLOCKED",
                                 requirements = ["[L161_ETCS2-TRK_sSyRS_00185]",
                                                 "[L161_ETCS2-TRK_sSyRS_00188]",
                                                 "[L161_ETCS2-TRK_sSyRS_00202]"],
                                 parameters = ["Route_Map/RM_interlocking_layer/connections/connection/locking_status"]) 
            sheet.ExpectedResult("SLR: SLR: For each <Referential/Route/Connections/Connection>, <Object_DYN_CONNECTION/connection/emergency_status> = TRUE (Only during one RBC cycle)",
                                 requirements = ["[L161_ETCS2-TRK_sSyRS_00188]",
                                                 "[L161_ETCS2-TRK_sSyRS_00202]"],
                                 parameters = ["Route_Map/RM_interlocking_layer/connections/connection/emergency_status"])
            sheet.ExpectedResult("SLR: SLR: For each <Referential/Route/Connections/Connection>, <Object_DYN_CONNECTION/connection/emergency_status> = FALSE (at the next cycle)")
            sheet.ExpectedResult("SLR: CES Message 15 is sent",
                                 requirements = ["[L161_ETCS2-TRK_sSyRS_00183]",
                                                 "[L161_ETCS2-TRK_sSyRS_00184]",
                                                 "[L161_ETCS2-TRK_sSyRS_00186]",
                                                 "[L161_ETCS2-TRK_sSyRS_00187]",
                                                 "[L161_ETCS2-TRK_sSyRS_00203]"])
            sheet.ExpectedResult("SLR: Ack of Emergency Stop Message 147 is received")
            sheet.ExpectedResult("SLR: CES Ack <Q_EMERGENCYSTOP> = 0 (CES accepted with update of EoA)")
        
sheet.Save()
