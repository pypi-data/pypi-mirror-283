from SheetCode import Sheet
import scripts.RT_Common as RT_Common

sheet = Sheet( __file__)

sheet.Name = "Conditional Emergency Stop on CSTR entrances"
sheet.Description = ["For each CSTR in <Referential/CSTR> and each route leading to this CSTR:",
                    "   - a train will be placed upstream of the start signal and the route will be set",
                    "   - the CSTR will be activated, which will close the start signal",
                    "   - RBC shall send a CES with a stopping location at the start signal"]

sheet.StartConditions = ["No elementary routes is set or locked.",
                          "No train is set on the track."]

for mode in ["FS", "OS", "SH"]:
    # *********************************************************************************************************************************************
    sheet.Case(f"Route set in {mode} to CSTR entrance")
    RT_Common.InitialConditionsL2(sheet, RT_Common.Aspects.RNP, RT_Common.InitialPositions.Valid)

    # ---------------------------------------------------------------------------------------------------------------------------------------------
    sheet.Action(f"Set route under test in {mode}")
    
    sheet.ExpectedResult("SLR: MA is received")  
    
    # ---------------------------------------------------------------------------------------------------------------------------------------------
    sheet.Action(f"Activate CSTR where this route leads")
    
    sheet.ExpectedResult("SLR: Conditional Emergency Stop Message 15 is sent",
                        requirements = ["[L161_ETCS2-TRK_sSyRS_00189]",
                                        "[L161_ETCS2-TRK_sSyRS_00190]"])
    
    sheet.ExpectedResult("SLR: CES <D_EMERGENCYSTOP> = <Referential/Route/DistanceLrbgToStartSignal>")
            
    sheet.ExpectedResult("SLR: For each <Referential/Route/Connections/Connection>, <Object_DYN_CONNECTION/connection/locking_status> = UNLOCKED",
                        requirements = ["[L161_ETCS2-TRK_sSyRS_00191]"],
                        parameters = ["LK/Output/Connections/locking_status_is_locked"])
    
    sheet.ExpectedResult("SLR: For each <Referential/Route/Connections/Connection>, <Object_DYN_CONNECTION/connection/emergency_status> = TRUE",
                        requirements = ["[L161_ETCS2-TRK_sSyRS_00191]"],
                        parameters = ["LK/Output/Connections/emergency_status"])
    
    sheet.ExpectedResult("SLR: If <Referential/Route/PossibleModes/OS> = TRUE:\nFor <Referential/Route/Connections/Connection>, <Object_DYN_CONNECTION/connection/permissivity> = ONSIGHT")
    
    sheet.ExpectedResult("SLR: If <Referential/Route/PossibleModes/SH> = TRUE:\nFor <Referential/Route/Connections/Connection>, <Object_DYN_CONNECTION/connection/permissivity> = SHUNT")
        
sheet.Save()
