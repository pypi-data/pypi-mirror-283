from SheetCode import Sheet
import scripts.RT_Common as RT_Common

sheet = Sheet(__file__)

sheet.Name = "Entry Routes"
sheet.Description = ["For each elementary route marked with Referential/Route/@Type='Entry' and in every applicable mode as per <Referential/Route/PossibleModes> (FS, OS or SH),",
                      "A train will be set upstream of the start signal in ETCS L1and the route will be set.",
                      "We will then check:",
                      "- MA (Length, Release Speed, Danger point, absence of section timers & overlap)",
                      "- Gradient profile",
                      "- Linking",
                      "- SSP for each category",
                      "- Mode profile (depending on mode set)",
                      "Then, train will drive past the start signal and the Level transition will be checked.",
                      "The aim of this test is not to test the whole transition trip starting from Registration BG, but only the first route. The full transition will be checked during functional tests."]

sheet.StartConditions = ["No elementary routes is set or locked.",
                          "No train is set on the track."]

for mode in ["FS", "OS", "SH"]:
    # *********************************************************************************************************************************************
    sheet.Case(f"Route set in {mode}")
    
    # ---------------------------------------------------------------------------------------------------------------------------------------------
    sheet.Action("Check initial conditions")
    sheet.ExpectedResult("SLR: All entry connections have <Object_DYN_CONNECTION/connection/locking_status> = LOCKED>",
                          requirements = ["[L161_ETCS2-TRK_sSyRS_00551]"]) 
    
    sheet.ExpectedResult("SLR: All other <Object_DYN_CONNECTION/connection/locking_status> = UNLOCKED>") 
    
    sheet.ExpectedResult("SLR: All <Object_DYN_TRACK_OCCUPATION/track_occupation/occupation_status> = RELEASED")
    
    sheet.ExpectedResult("SLR: All <Object_DYN_BOUNDARY/boundary/activation_status> = ENFORCED",
                         requirements = ["[L161_ETCS2-TRK_sSyRS_00546]"])
    
    # ---------------------------------------------------------------------------------------------------------------------------------------------
    sheet.Action("Set a train on the route <Referential/Route/@Name>, with Unknown LRBG and perform SoM in L1")
    sheet.ExpectedResult("EOnBE: OBU is in Level 1 Mode SR")
    
    # ---------------------------------------------------------------------------------------------------------------------------------------------
    sheet.Action("Cross BG-N balise group")
    sheet.ExpectedResult("EOnBE: OBU registers on GSM-R network before reaching BG-E")
    
    # ---------------------------------------------------------------------------------------------------------------------------------------------
    sheet.Action("Cross BG-E balise group")
    sheet.ExpectedResult("EOnBE: OBU connects to RBC before reaching L2 border")
    sheet.ExpectedResult("SLR: Position Report with <M_LEVEL> = 2 (Level 1)")
    sheet.ExpectedResult("SLR: Position Report with <M_MODE> = 2 (Staff Responsible)")
    sheet.ExpectedResult("SLR: Position Report with <LRBG> = BG-E")
    
    # ---------------------------------------------------------------------------------------------------------------------------------------------
    sheet.Action("Cross BG-E' balise group")
    sheet.ExpectedResult("SLR: Position Report with <LRBG> = BG-E'")
    
    # ---------------------------------------------------------------------------------------------------------------------------------------------
    sheet.Action("Cross SBG of Signal 0")
    sheet.ExpectedResult("SLR: Position Report with <M_LEVEL> = 2 (Level 1) - No change")
    sheet.ExpectedResult("SLR: Position Report with <M_MODE> = 0 (Full Supervision)")
    sheet.ExpectedResult("SLR: Position Report with <LRBG> = SBG of Signal 0")
    # ---------------------------------------------------------------------------------------------------------------------------------------------
    sheet.Action(f"Set route under test in {mode}")
    sheet.ExpectedResult("Route is set for entry in L2 area")
    # ---------------------------------------------------------------------------------------------------------------------------------------------
    sheet.Action("Cross BG-A balise group (entry balise group)")
    sheet.ExpectedResult("SLR: Position Report with <NID_LRBG> = <Referential/Route/LRBG> (=BG-A which will be the trigger to send MA)",
                          requirements = ["[L161_ETCS2-TRK_sSyRS_00519]",
                                          "[L161_ETCS2-TRK_sSyRS_00515]"],
                          parameters = ["Route_Map/RM_RTM_layer/balise_groups/entry_balise_group/id"])
    
    sheet.ExpectedResult("SLR: <Object_DYN_TRAIN_DATA/one_Train_Data/train_state> = ENTERING",
                          requirements = ["[L161_ETCS2-TRK_sSyRS_00524]",
                                        "[L161_ETCS2-TRK_sSyRS_00642]"])
    
    sheet.ExpectedResult("SLR: <Object_DYN_TRAIN_DATA/one_Train_Data/elementary_conditions/EC_packet_9_available> = false",
                          requirements = ["[L161_ETCS2-TRK_sSyRS_00641]"],
                          parameters = ["Route_Map/RM_RTM_layer/boundaries/boundary/packet_9_used"])

   # Check MA, Gradient, Linking, SSP and MP
    RT_Common.ExpectedResultsRouteCommons(sheet, mode)
    
    sheet.ExpectedResult("SLR: Level Transition Order Packet 41 is sent to ENTERING train",
                          requirements = ["[L161_ETCS2-TRK_sSyRS_00518]",
                                          "[L161_ETCS2-TRK_sSyRS_00525]",
                                          "[L161_ETCS2-TRK_sSyRS_00680]"])
    
    sheet.ExpectedResult("SLR: Level Transition Order <D_LEVELTR> = <Referential/Route/LevelTransitionOrderPacket/D_LEVELTR>",
                          parameters = ["Route_Map/RM_RTM_layer/balise_groups/entry_balise_group/direction",
                                        "Route_Map/RM_RTM_layer/balise_groups/entry_balise_group/distance_to_boundary",
                                        "Route_Map/RM_RTM_layer/boundaries/boundary/location/offset",
                                        "Route_Map/RM_RTM_layer/boundaries/boundary/location/segment_id"])
    
    sheet.ExpectedResult("SLR: Level Transition Order <N_ITER> = Count of <Referential/Route/LevelTransitionOrderPacket/Iterations> - 1",
                          parameters = ["Route_Map/RM_RTM_layer/boundaries/boundary/N_area_available_levels"])
                        
    sheet.ExpectedResult("SLR: Level Transition Order <M_LEVELTR> = <Referential/Route/LevelTransitionOrderPacket/Iterations/M_LEVELTR> (all instances in order)",
                          requirements = ["[L161_ETCS2-TRK_sSyRS_00528]",
                                          "[L161_ETCS2-TRK_sSyRS_00526]",
                                          "[L161_ETCS2-TRK_sSyRS_00527]"],
                          parameters = ["Route_Map/RM_RTM_layer/boundaries/boundary/Area_available_levels/entering_level"])
    
    sheet.ExpectedResult("SLR: Level Transition Order <NID_NTC> = <Referential/Route/LevelTransitionOrderPacket/Iterations/NID_NTC> (all instances in order)",
                          requirements = ["[L161_ETCS2-TRK_sSyRS_00528]",
                                          "[L161_ETCS2-TRK_sSyRS_00526]",
                                          "[L161_ETCS2-TRK_sSyRS_00501]"],
                          parameters = ["Route_Map/RM_RTM_layer/boundaries/boundary/Area_available_levels/entering_nid_STM"])
    
    sheet.ExpectedResult("SLR: Level Transition Order <L_ACKLEVELTR> = 0 meters (all instances in order)",
                          requirements = ["[L161_ETCS2-TRK_sSyRS_00529]"],
                          parameters = ["Route_Map/RM_RTM_layer/boundaries/boundary/Area_available_levels/acknowledgement_distance"])
    
    # ---------------------------------------------------------------------------------------------------------------------------------------------
    sheet.Action("Cross the BG-T Balise group")
    sheet.ExpectedResult("SLR: Position Report with <M_LEVEL> = 3 (Level 2)",
                          requirements = ["[L161_ETCS2-TRK_sSyRS_00534]"])
    if mode == "FS":
        sheet.ExpectedResult("SLR: Position Report with <M_MODE> = 0 (Full supervision)")
    if mode == "OS":
        sheet.ExpectedResult("SLR: Position Report with <M_MODE> = 1 (Onsight)")
    elif mode == "SH":
        sheet.ExpectedResult("SLR: Position Report with <M_MODE> = 3 (Shunting)")
    
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


sheet.Save()









