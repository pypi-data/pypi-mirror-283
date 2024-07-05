from SheetCode import Sheet
import scripts.RT_Common as RT_Common
import libs.Referential as Referential

sheet = Sheet(__file__)

sheet.Name = "Conditional Emergency Stop due to signal replacement"
sheet.Description = ["For each elementary route marked with Referential/Route/@Type='Inside' and in every applicable mode as per <Referential/Route/PossibleModes> (FS, OS or SH).",
                      "1) a train is placed upstream of the start signal and the route is set in each mode. We are not checking the MA content as it's done already in RT_* tests",
                      "   In order to test CES_shift_maximum_distance = 7m, we set a L_DOUBTOVER = 8m, so that a lower doubt-over won't mask the parameter effect."
                      "2) The track downstream is occupied We check that:",
                      "   - CES is sent with a stopping point at the start signal, minus 7m (CES_shift_maximum_distance)",
                      "   - CES is accepted by the train as MSFE is upstream of the stopping point.",
                      "   - CES is then immediately revoked",
                      "Note: Signal replacement is valid for all signal types."]

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
            sheet.Action(f"Set train L_DOUBTOVER to 8m (CES_shift_maximum_distance + 1m")
            sheet.ExpectedResult("SLR: Position Report with <L_DOUBTOVER> = 8 m")

            # ---------------------------------------------------------------------------------------------------------------------------------------------
            sheet.Action(f"Set route under test in {mode}")
            sheet.ExpectedResult("SLR: MA is sent")
            
            # ---------------------------------------------------------------------------------------------------------------------------------------------
            sheet.Action(f"Occupy the next track downstream")
            sheet.ExpectedResult("SLR: SLR: For each <Referential/Route/Connections/Connection>, <Object_DYN_CONNECTION/connection/locking_status> = UNLOCKED",
                                 requirements = ["[L161_ETCS2-TRK_sSyRS_00178]",
                                                 "[L161_ETCS2-TRK_sSyRS_00605]",
                                                 "[L161_ETCS2-TRK_sSyRS_00608]"],
                                 parameters = ["Route_Map/RM_interlocking_layer/connections/connection/locking_status"]) 
            sheet.ExpectedResult("SLR: SLR: For each <Referential/Route/Connections/Connection>, <Object_DYN_CONNECTION/connection/emergency_status> = TRUE (Only during one RBC cycle)",
                                 requirements = ["[L161_ETCS2-TRK_sSyRS_00178]",
                                                 "[L161_ETCS2-TRK_sSyRS_00179]",
                                                 "[L161_ETCS2-TRK_sSyRS_00605]",
                                                 "[L161_ETCS2-TRK_sSyRS_00608]"],
                                 parameters = ["Route_Map/RM_interlocking_layer/connections/connection/emergency_status"])
            sheet.ExpectedResult("SLR: SLR: For each <Referential/Route/Connections/Connection>, <Object_DYN_CONNECTION/connection/emergency_status> = FALSE (at the next cycle)",
                                 requirements = ["[L161_ETCS2-TRK_sSyRS_00179]"],
                                 parameters = ["Route_Map/RM_interlocking_layer/connections/connection/emergency_status"])
            sheet.ExpectedResult("SLR: CES Message 15 is sent",
                                 requirements = ["[L161_ETCS2-TRK_sSyRS_00176]",
                                                 "[L161_ETCS2-TRK_sSyRS_00177]",
                                                 "[L161_ETCS2-TRK_sSyRS_00183]",
                                                 "[L161_ETCS2-TRK_sSyRS_00203]",
                                                 "[L161_ETCS2-TRK_sSyRS_00243]",
                                                 "[L161_ETCS2-TRK_sSyRS_00604]",
                                                 "[L161_ETCS2-TRK_sSyRS_00607]"])
            sheet.ExpectedResult("SLR: CES <D_EMERGENCYSTOP> = <Referential/Route/MovementAuthorityPacket/DistanceLrbgToStartSignal> - 7m (CES_shift_maximum_distance)",
                                 requirements = ["[L161_ETCS2-TRK_sSyRS_00180]",
                                                 "[L161_ETCS2-TRK_sSyRS_00204]",
                                                 "[L161_ETCS2-TRK_sSyRS_00210]",
                                                 "[L161_ETCS2-TRK_sSyRS_00222]"])
            sheet.ExpectedResult("SLR: Ack of Emergency Stop Message 147 is received")
            sheet.ExpectedResult("SLR: CES Ack <Q_EMERGENCYSTOP> = 0 (CES accepted with update of EoA)",
                                 requirements = ["[L161_ETCS2-TRK_sSyRS_00218]"])
            sheet.ExpectedResult("SLR: CES Ack <NID_EM> = X (Save the value for later")
            sheet.ExpectedResult("SLR: No more CES Message 15 is sent",
                                 requirements = ["[L161_ETCS2-TRK_sSyRS_00220]"])
            sheet.ExpectedResult("SLR: Revocation of Emergency Stop Message 18 is sent",
                                 requirements = ["[L161_ETCS2-TRK_sSyRS_00205]"])
            sheet.ExpectedResult("SLR: Revocation of Emergency Stop Message 18 is sent",
                                 requirements = ["[L161_ETCS2-TRK_sSyRS_00205]"])
            sheet.ExpectedResult("SLR: Revocation <NID_EM> = X (Same as CES)",
                                 requirements = ["[L161_ETCS2-TRK_sSyRS_00206]",
                                                 "[L161_ETCS2-TRK_sSyRS_00207]"])
            sheet.ExpectedResult("SLR: Acknowledgement Message 146 is received")
            sheet.ExpectedResult("SLR: No more Revocation of Emergency Stop Message 18 is sent",
                                 requirements = ["[L161_ETCS2-TRK_sSyRS_00219]",
                                                 "[L161_ETCS2-TRK_sSyRS_00220]"])
            if mode == "OS":
                sheet.ExpectedResult("SLR: Movement Authority Message 3 with Mode profile packet 80 is sent")             
                sheet.ExpectedResult("SLR: Mode profile <N_ITER> = 1 (Two OS mode profile segments)",
                                 requirements = ["[L161_ETCS2-TRK_sSyRS_00609]"])
            else:
                sheet.ExpectedResult("SLR: No Movement Authority Message 3 is sent")  
sheet.Save()
