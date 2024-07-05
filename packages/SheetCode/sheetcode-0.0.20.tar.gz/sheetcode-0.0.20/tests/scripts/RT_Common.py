from enum import Enum

class Modes(Enum):
    FS = "Full Supervision"
    OS = "Onsight"
    SR = "Staff Responsible"
    SH = "Shunting"
    SN = "National System"
    
class Aspects(Enum):
    RNP = 0
    RP = 1
    RW = 2
    PROCEED = 3
    
class InitialPositions(Enum):
    Invalid = 0
    Valid = 1
    Unknown = 2


def InitialConditionsL2(sheet, aspect, initialPosition:InitialPositions):
    # ---------------------------------------------------------------------------------------------------------------------------------------------
    sheet.Action("Check initial conditions")
    
    sheet.ExpectedResult("SLR: All entry connections have <Object_DYN_CONNECTION/connection/locking_status> = LOCKED>") 
    sheet.ExpectedResult("SLR: All connections associated to Non-Automatic signals have <Object_DYN_CONNECTION/connection/locking_status> = UNLOCKED>") 
    sheet.ExpectedResult("SLR: All connections associated to Automatic signals have <Object_DYN_CONNECTION/connection/locking_status> = LOCKED> (As Track Occupations downstream are released)") 
    sheet.ExpectedResult("SLR: All <Object_DYN_TRACK_OCCUPATION/occupation_statuses/occupation_status> = RELEASED")
    
    # ---------------------------------------------------------------------------------------------------------------------------------------------
    sheet.Action("Place a train on the route <Referential/Route/@Name>, reporting on the <Referential/Route/LRBG> with a VALID position and perform SoM in L2")
    
    if initialPosition == InitialPositions.Invalid:
        sheet.ExpectedResult("SLR: SoM Position Report with <Q_STATUS> = 0 (Invalid)")
    elif initialPosition == InitialPositions.Valid:
        sheet.ExpectedResult("SLR: SoM Position Report with <Q_STATUS> = 1 (Valid)")
    elif initialPosition == InitialPositions.Unknown:
        sheet.ExpectedResult("SLR: SoM Position Report with <Q_STATUS> = 2 (Unknown)")
        
    if aspect == Aspects.RP or aspect == Aspects.RW or aspect == Aspects.PROCEED:
        sheet.ExpectedResult("SLR: Movement Authority Message 3 with Mode profile packet 80 is sent")             
        sheet.ExpectedResult("SLR: Mode Profile <L_MAMODE> = <Referential/Route/MovementAuthorityPacket/DistanceLrbgToStartSignal> (OS up to start signal)",
                             requirements = ["[L161_ETCS2-TRK_sSyRS_00093]"])
        sheet.ExpectedResult("SLR: Position Report with <M_MODE> = 1 (Onsight)")
        sheet.ExpectedResult("SLR: National Values Packet 3 are received within MA.\nNote: Check of NV values is done in SOM test.",
                            requirements = ["[L161_ETCS2-TRK_sSyRS_00429]"])
    elif aspect == Aspects.RNP:
        sheet.ExpectedResult("SLR: SR Authorisation Message 2 is sent",
                            requirements = ["[L161_ETCS2-TRK_sSyRS_00099]",
                                            "[L161_ETCS2-TRK_sSyRS_00100]"])  
        sheet.ExpectedResult("SLR: Position Report with <M_MODE> = 2 (Staff Responsible)")
    
    sheet.ExpectedResult("SLR: Position Report with <M_LEVEL> = 3 (Level 2)")
    sheet.ExpectedResult("SLR: Position Report with <NID_LRBG> = <Referential/Route/LRBG>")
    sheet.ExpectedResult("SLR: For each <Referential/Route/ModeProfiles/ModeProfile/@Name>, <Object_DYN_MPS/predefined_MP/MP_activation_status> = DISABLED")

def ExpectedResultsRouteCommons(sheet, aspect):
    # Check connections locking status                         
    sheet.ExpectedResult("SLR: For each <Referential/Route/Connections/Connection>, <Object_DYN_CONNECTION/connection/locking_status> = LOCKED",
                          requirements = ["[L161_ETCS2-TRK_sSyRS_00263]",
                                          "[L161_ETCS2-TRK_sSyRS_00265]"],
                          parameters = ["LK/Output/Connections/locking_status_is_locked",
                                        "Route_Map/RM_interlocking_layer/points/point/left_connector_id",
                                        "Route_Map/RM_interlocking_layer/points/point/right_connector_id"])
    sheet.ExpectedResult("SLR: For all other connections, <Object_DYN_CONNECTION/connection/locking_status> = UNLOCKED",
                          parameters = ["Route_Map/RM_interlocking_layer/connections/connection/locking_status"])  
    
    # Check points                         
    sheet.ExpectedResult("SLR: For each <Referential/Route/Points/Point>, <Object_DYN_POINT/point/IXL_point_position> = <Referential/Route/Points/Point/Position",
                          requirements = ["[L161_ETCS2-TRK_sSyRS_00591]",
                                          "[L161_ETCS2-TRK_sSyRS_00556]",
                                          "[L161_ETCS2-TRK_sSyRS_00557]",
                                          "[L161_ETCS2-TRK_sSyRS_00558]",
                                          "[L161_ETCS2-TRK_sSyRS_00672]"],
                          parameters = ["Route_Map/RM_interlocking_layer/points/point/IXL_point_position",
                                        "LK/Output/Points/ixl_pt_position_is_right",
                                        "LK/Output/Points/ixl_pt_position_is_left"])
    
    sheet.ExpectedResult("SLR: For each <Referential/Route/Points/Point>, <Object_DYN_POINT/point/IXL_point_state> = NO_LOCAL_CONTROL",
                          parameters = ["Route_Map/RM_interlocking_layer/points/point/IXL_point_state"])
    
    if aspect == Aspects.PROCEED:
        # Check connections permissivity
        sheet.ExpectedResult("SLR: For each <Referential/Route/Connections/Connection>, <Object_DYN_CONNECTION/connection/permissivity> = NONE",
                              parameters = ["Route_Map/RM_interlocking_layer/connections/connection/permissivity"])
        
        # Check mode profiles                         
        sheet.ExpectedResult("SLR: For all Mode Profiles <Object_DYN_MPS/predefined_MP/MP_activation_status> = DISABLED, except the MP of the current track section",
                              requirements = ["[L161_ETCS2-TRK_sSyRS_00263]",
                                              "[L161_ETCS2-TRK_sSyRS_00269]"])

        # MA
        sheet.Action("Check Movement Authority packet 15")
        
        sheet.ExpectedResult("SLR: MA packet 15 is sent",
                            requirements = ["[L161_ETCS2-TRK_sSyRS_00237]",
                                            "[L161_ETCS2-TRK_sSyRS_00241]",
                                            "[L161_ETCS2-TRK_sSyRS_00244]"])
        
        sheet.ExpectedResult("SLR: MA <L_ENDSECTION> = <Referential/Route/MovementAuthorityPacket/DistanceLrbgToEndSignal>", 
                            requirements = ["[L161_ETCS2-TRK_sSyRS_00141]",
                                            "[L161_ETCS2-TRK_sSyRS_00143]",
                                            "[L161_ETCS2-TRK_sSyRS_00248]",
                                            "[L161_ETCS2-TRK_sSyRS_00260]",
                                            "[L161_ETCS2-TRK_sSyRS_00261]",
                                            "[L161_ETCS2-TRK_sSyRS_00262]",
                                            "[L161_ETCS2-TRK_sSyRS_00305]"],
                            parameters = [  "Route_Map/RM_track_layout/segments/segment/length",
                                            "Route_Map/RM_track_layout/segments/segment/norm_dir_node_id",
                                            "Route_Map/RM_track_layout/segments/segment/rev_dir_node_id",
                                            "Route_Map/RM_track_layout/connectors/connector/norm_dir_node_id",
                                            "Route_Map/RM_track_layout/connectors/connector/rev_dir_node_id",
                                            "Route_Map/RM_interlocking_layer/connections/connection/direction", 
                                            "Route_Map/RM_interlocking_layer/connections/connection/stopping_point_id",
                                            "Route_Map/RM_interlocking_layer/connections/connection/connector_id",
                                            "Route_Map/RM_interlocking_layer/connections/connection/overlap_id",
                                            "Route_Map/RM_interlocking_layer/stopping_points/stopping_point/location/offset",
                                            "Route_Map/RM_track_layout/nodes/node/kilometric_point"])

        sheet.ExpectedResult("SLR: MA <V_LOA> = 0",
                            requirements = ["[L161_ETCS2-TRK_sSyRS_00672]"])

        sheet.ExpectedResult("SLR: MA <T_LOA> = 0")
        
        sheet.ExpectedResult("SLR: MA <N_ITER> = 0",
                            requirements = ["[L161_ETCS2-TRK_sSyRS_00674]"]) 

        sheet.ExpectedResult("SLR: MA <V_RELEASEDP> = <Referential/Route/MovementAuthorityPacket/V_RELEASEDP>",
                            requirements = ["[L161_ETCS2-TRK_sSyRS_00245]",
                                            "[L161_ETCS2-TRK_sSyRS_00368]"],
                            parameters = ["Route_Map/RM_interlocking_layer/danger_points/danger_point/v_releasedp"]) 

        sheet.ExpectedResult("SLR: MA <D_DP> = 0 (0 meters)",
                            requirements = ["[L161_ETCS2-TRK_sSyRS_00142]",
                                            "[L161_ETCS2-TRK_sSyRS_00144]",
                                            "[L161_ETCS2-TRK_sSyRS_00675]"],
                            parameters = ["Route_Map/RM_interlocking_layer/danger_points/danger_point/location/segment_id",
                                          "Route_Map/RM_interlocking_layer/danger_points/danger_point/location/offset",                                          
                                          "Route_Map/RM_interlocking_layer/connections/connection/danger_point_id"]) 

        sheet.ExpectedResult("SLR: MA <Q_OVERLAP> = 0 (No overlap)",
                            requirements = ["[L161_ETCS2-TRK_sSyRS_00153]"],
                            parameters = ["Route_Map/RM_interlocking_layer/connections/connection/selected_overlap"]) 

        sheet.ExpectedResult("SLR: MA <Q_SECTIONTIMER> = 0 (No section timer)",
                            requirements = ["[L161_ETCS2-TRK_sSyRS_00152]"],
                            parameters = ["Route_Map/RM_interlocking_layer/connections/connection/t_section_timer",
                                        "Route_Map/RM_interlocking_layer/connections/connection/d_sectiontimerstoploc"]) 

        sheet.ExpectedResult("SLR: MA <Q_ENDTIMER> = 0 (No end timer)",
                            requirements = ["[L161_ETCS2-TRK_sSyRS_00152]"],
                            parameters = ["Route_Map/RM_interlocking_layer/connections/connection/t_endtimer",
                                        "Route_Map/RM_interlocking_layer/connections/connection/d_endtimerstartloc"]) 
        
        # Gradient
        sheet.Action("Check Gradient profile packet 21")
        sheet.ExpectedResult("SLR: Gradient profile packet 21 is sent",
                            requirements = ["[L161_ETCS2-TRK_sSyRS_00237]",
                                            "[L161_ETCS2-TRK_sSyRS_00258]",
                                            "[L161_ETCS2-TRK_sSyRS_00679]",])
        sheet.ExpectedResult("SLR: Gradient Profile <D_GRADIENT> = <Referential/Route/GradientProfilePacket/Gradient/D_GRADIENT> (all instances in order)",
                            requirements = ["[L161_ETCS2-TRK_sSyRS_00590]",],
                            parameters = [  "Route_Map/RM_civil_characteristics_layer/gradients/gradient/start_location/offset",
                                            "Route_Map/RM_civil_characteristics_layer/gradients/gradient/start_location/qdir",
                                            "Route_Map/RM_civil_characteristics_layer/gradients/gradient/start_location/segment_id",
                                            "Route_Map/RM_civil_characteristics_layer/gradients/gradient/end_location/offset",
                                            "Route_Map/RM_civil_characteristics_layer/gradients/gradient/end_location/qdir",
                                            "Route_Map/RM_civil_characteristics_layer/gradients/gradient/end_location/segment_id"])

        sheet.ExpectedResult("SLR: Gradient Profile <G_A> with sign <Q_GDIR> = <Referential/Route/GradientProfilePacket/Gradient/Q_GDIR> (all instances in order)",
                            requirements = ["[L161_ETCS2-TRK_sSyRS_00676]",
                                            "[L161_ETCS2-TRK_sSyRS_00677]"],
                            parameters = ["Route_Map/RM_civil_characteristics_layer/gradients/gradient/slope"])

        # Linking
        sheet.Action("Check Linking profile packet 5")
        sheet.ExpectedResult("SLR: Linking profile packet 5 is sent",
                            requirements = ["[L161_ETCS2-TRK_sSyRS_00237]",
                                            "[L161_ETCS2-TRK_sSyRS_00362]"])
        
        sheet.ExpectedResult("SLR: Linking <NID_C> = <Referential/Route/LinkingProfilePacket/Linking/NID_C> (all instances in order)",
                            parameters = ["Route_Map/RM_RTM_layer/balise_groups/balise_group/id"])

        sheet.ExpectedResult("SLR: Linking <NID_BG> = <Referential/Route/LinkingProfilePacket/Linking/NID_BG> (all instances in order)",
                            requirements = ["[L161_ETCS2-TRK_sSyRS_00377]"],
                            parameters = ["Route_Map/RM_RTM_layer/balise_groups/balise_group/id"])

        sheet.ExpectedResult("SLR: Linking <D_LINK> = <Referential/Route/LinkingProfilePacket/Linking/D_LINK> (all instances in order)",
                            parameters = ["Route_Map/RM_RTM_layer/balise_groups/balise_group/location/segment_id",
                                          "Route_Map/RM_RTM_layer/balise_groups/balise_group/location/offset"])

        sheet.ExpectedResult("SLR: Linking <Q_LINKORIENTATION> = <Referential/Route/LinkingProfilePacket/Linking/Q_LINKORIENTATION> (all instances in order)",
                            parameters = ["Route_Map/RM_RTM_layer/balise_groups/balise_group/direction"])

        sheet.ExpectedResult("SLR: Linking <Q_LOCACC> = <Referential/Route/LinkingProfilePacket/Linking/Q_LOCACC> (all instances in order)",
                            requirements = ["[L161_ETCS2-TRK_sSyRS_00363]",
                                            "[L161_ETCS2-TRK_sSyRS_00364]"],
                            parameters = ["Route_Map/RM_RTM_layer/balise_groups/balise_group/installation_accuracy"])
        
        sheet.ExpectedResult("SLR: Linking <Q_LINKREACTION> = <Referential/Route/LinkingProfilePacket/Linking/Q_LINKREACTION> (all instances in order)",
                            requirements = ["[L161_ETCS2-TRK_sSyRS_00365]"],
                            parameters = ["Route_Map/RM_RTM_layer/balise_groups/balise_group/q_linkreaction"])

        # SSP
        sheet.Action("Check SSP packet 27")
        sheet.ExpectedResult("SLR: SSP packet 27 is sent",
                            requirements = ["[L161_ETCS2-TRK_sSyRS_00237]"])
        sheet.ExpectedResult(f"SLR: SSP <D_STATIC> = <Referential/InternationalStaticSpeedProfilePacket/Category/StaticSpeed/D_STATIC> (all instances in order)",
                            parameters = [  "Route_Map/RM_civil_characteristics_layer/SSPs/SSP/start_location/offset",
                                            "Route_Map/RM_civil_characteristics_layer/SSPs/SSP/start_location/qdir",
                                            "Route_Map/RM_civil_characteristics_layer/SSPs/SSP/start_location/segment_id",
                                            "Route_Map/RM_civil_characteristics_layer/SSPs/SSP/end_location/offset",
                                            "Route_Map/RM_civil_characteristics_layer/SSPs/SSP/end_location/qdir",
                                            "Route_Map/RM_civil_characteristics_layer/SSPs/SSP/end_location/segment_id"])

        sheet.ExpectedResult(f"SLR: SSP <V_STATIC> = Minimum between all <Referential/InternationalStaticSpeedProfilePacket/Category/StaticSpeed/V_DIFF> (all instances in order)",
                            requirements = ["[L161_ETCS2-TRK_sSyRS_00251]",
                                            "[L161_ETCS2-TRK_sSyRS_00252]",
                                            "[L161_ETCS2-TRK_sSyRS_00253]",
                                            "[L161_ETCS2-TRK_sSyRS_00256]",
                                            "[L161_ETCS2-TRK_sSyRS_00257]"],
                            parameters = ["Route_Map/RM_civil_characteristics_layer/SSPs/SSP/v_static"])

        sheet.ExpectedResult(f"SLR: SSP <Q_FRONT> = <Referential/InternationalStaticSpeedProfilePacket/Category/StaticSpeed/Q_FRONT> (all instances in order)",
                            requirements = ["[L161_ETCS2-TRK_sSyRS_00254]"],
                            parameters = ["Route_Map/RM_civil_characteristics_layer/SSPs/SSP/train_length_delay"])
                                            
        sheet.ExpectedResult(f"SLR: SSP <NC_DIFF> = <Referential/InternationalStaticSpeedProfilePacket/Category/@NC_DIFF]> (each category)",
                            parameters = ["Route_Map/RM_civil_characteristics_layer/SSPs/SSP/other_specific_cat/SSP_category_type"])

        sheet.ExpectedResult(f"SLR: SSP <V_DIFF> = <Referential/InternationalStaticSpeedProfilePacket/Category/StaticSpeed/V_DIFF]> (for each category, all instances in order)",
                            requirements = ["[L161_ETCS2-TRK_sSyRS_00257]"],
                            parameters = ["Route_Map/RM_civil_characteristics_layer/SSPs/SSP/speed_level"])
        
        # Check absence of packets
        sheet.Action("Check absence of packets")    
        sheet.ExpectedResult("SLR: Axle load Speed profile packet 51 is NOT sent",
                              requirements = ["[L161_ETCS2-TRK_sSyRS_00238]"])
        sheet.ExpectedResult("SLR: Route Suitability Data packet 70 is NOT sent",
                              parameters = ["Route_Map/RM_interlocking_layer/connections/connection/selected_suitability"],
                              requirements = ["[L161_ETCS2-TRK_sSyRS_00238]"])
        
        # Check mode profiles  
        sheet.Action("Check Mode profile Packet 80")    
        sheet.ExpectedResult("SLR: Mode profile packet 80 is sent",
                            requirements = ["[L161_ETCS2-TRK_sSyRS_00237]",
                                            "[L161_ETCS2-TRK_sSyRS_00263]",
                                            "[L161_ETCS2-TRK_sSyRS_00268]",
                                            "[L161_ETCS2-TRK_sSyRS_00309]",
                                            "[L161_ETCS2-TRK_sSyRS_00681]"]) 
        sheet.ExpectedResult("SLR: Mode profile <N_ITER> = 0 (One OS mode profile segment only)",
                            requirements = ["[L161_ETCS2-TRK_sSyRS_00095]",
                                            "[L161_ETCS2-TRK_sSyRS_00096]"])               
        sheet.ExpectedResult("SLR: Mode Profile <L_MAMODE> = <Referential/Route/MovementAuthorityPacket/DistanceLrbgToStartSignal> (OS is not extended to next route)",
                            requirements=["[L161_ETCS2-TRK_sSyRS_00682]"])
        sheet.ExpectedResult("SLR: Mode profile <M_MAMODE> = 0 (Onsight)")

        
    elif aspect == Aspects.RP or aspect == Aspects.RW:
                                
        sheet.ExpectedResult("SLR: For each <Referential/Route/ModeProfiles/ModeProfile/@Name>, <Object_DYN_MPS/predefined_MP/MP_activation_status> = ENFORCED",
                              parameters = ["LK/Output/Mode profiles/MP_activation_enforced"])

        # MP
        if aspect == Aspects.RP:
            # Specific checks for OS
            
            # Check connections permissivity
            sheet.ExpectedResult("SLR: Only one (1) connection <Referential/Route/Connections/Connection> has <Object_DYN_CONNECTION/connection/permissivity> = ONSIGHT",
                              requirements = ["[L161_ETCS2-TRK_sSyRS_00277]"],
                              parameters = ["LK/Output/Connections/permissivity_is_OS"])
        
            sheet.ExpectedResult("SLR: For each <Referential/Route/ModeProfiles/ModeProfile/@Name>, <Object_DYN_MPS/predefined_MP/permissivity> = ONSIGHT")

            sheet.Action("Check Mode profile Packet 80")
            
            sheet.ExpectedResult("SLR: Mode profile <N_ITER> = 1 (Two OS mode profile segments)",
                        requirements = ["[L161_ETCS2-TRK_sSyRS_00094]"])
            
            sheet.ExpectedResult("SLR: Mode profile Packet 80 is sent",
                                requirements = ["[L161_ETCS2-TRK_sSyRS_00681]"])

            sheet.ExpectedResult("SLR: Mode profile <D_MAMODE> / Iteration #1 = 0",
                                requirements = ["[L161_ETCS2-TRK_sSyRS_00091]",
                                                "[L161_ETCS2-TRK_sSyRS_00682]",
                                                "[L161_ETCS2-TRK_sSyRS_00094]"],
                                parameters= ["Route_Map/RM_operational_conditions_layer/MPs/MP/start_location/offset",
                                            "Route_Map/RM_operational_conditions_layer/MPs/MP/start_location/qdir",
                                            "Route_Map/RM_operational_conditions_layer/MPs/MP/start_location/segment_id"])

            sheet.ExpectedResult("SLR: Mode profile <L_MAMODE> / Iteration #1 = <Referential/Route/MovementAuthorityPacket/DistanceLrbgToStartSignal>",
                                requirements = ["[L161_ETCS2-TRK_sSyRS_00285]", 
                                                "[L161_ETCS2-TRK_sSyRS_00286]", 
                                                "[L161_ETCS2-TRK_sSyRS_00287]",
                                                "[L161_ETCS2-TRK_sSyRS_00266]",
                                                "[L161_ETCS2-TRK_sSyRS_00267]",
                                                "[L161_ETCS2-TRK_sSyRS_00682]"],
                                parameters= ["Route_Map/RM_operational_conditions_layer/MPs/MP/end_location/offset",
                                            "Route_Map/RM_operational_conditions_layer/MPs/MP/end_location/qdir",
                                            "Route_Map/RM_operational_conditions_layer/MPs/MP/end_location/segment_id"])

            sheet.ExpectedResult("SLR: Mode profile <M_MAMODE> / Iteration #1  = 0 (Onsight)",
                                parameters = ["Route_Map/RM_operational_conditions_layer/MPs/MP/mp_mode"])
            
            sheet.ExpectedResult("SLR: Mode profile <D_MAMODE> / Iteration #2 = <Referential/Route/MovementAuthorityPacket/DistanceLrbgToStartSignal>",
                                requirements = ["[L161_ETCS2-TRK_sSyRS_00091]",
                                                "[L161_ETCS2-TRK_sSyRS_00682]",
                                                "[L161_ETCS2-TRK_sSyRS_00094]"],
                                parameters= ["Route_Map/RM_operational_conditions_layer/MPs/MP/start_location/offset",
                                            "Route_Map/RM_operational_conditions_layer/MPs/MP/start_location/qdir",
                                            "Route_Map/RM_operational_conditions_layer/MPs/MP/start_location/segment_id"])

            sheet.ExpectedResult("SLR: Mode profile <L_MAMODE> / Iteration #1 = <Referential/Route/MovementAuthorityPacket/DistanceLrbgToEndSignal> - <Referential/Route/MovementAuthorityPacket/DistanceLrbgToStartSignal>",
                                requirements = ["[L161_ETCS2-TRK_sSyRS_00285]", 
                                                "[L161_ETCS2-TRK_sSyRS_00286]", 
                                                "[L161_ETCS2-TRK_sSyRS_00287]",
                                                "[L161_ETCS2-TRK_sSyRS_00266]",
                                                "[L161_ETCS2-TRK_sSyRS_00267]",
                                                "[L161_ETCS2-TRK_sSyRS_00682]"],
                                parameters= ["Route_Map/RM_operational_conditions_layer/MPs/MP/end_location/offset",
                                            "Route_Map/RM_operational_conditions_layer/MPs/MP/end_location/qdir",
                                            "Route_Map/RM_operational_conditions_layer/MPs/MP/end_location/segment_id"])

            sheet.ExpectedResult("SLR: Mode profile <M_MAMODE> / Iteration #1  = 0 (Onsight)",
                                parameters = ["Route_Map/RM_operational_conditions_layer/MPs/MP/mp_mode"])

        if aspect == Aspects.RW:
            # Specific checks for SH
            
            # Check connections permissivity
            sheet.ExpectedResult("SLR: For each <Referential/Route/Connections/Connection>, <Object_DYN_CONNECTION/connection/permissivity> = SHUNT",
                                requirements = ["[L161_ETCS2-TRK_sSyRS_00265]"],
                                parameters = ["LK/Output/Connections/permissivity_is_SH"])
            
            sheet.ExpectedResult("SLR: For each <Referential/Route/ModeProfiles/ModeProfile/@Name>, <Object_DYN_MPS/predefined_MP/permissivity> = SHUNT")
            
            sheet.Action("Check Mode profile Packet 80")
            
            sheet.ExpectedResult("SLR: Mode profile Packet 80 is sent",
                                requirements = ["[L161_ETCS2-TRK_sSyRS_00681]"])
            
            sheet.ExpectedResult("SLR: Mode profile <N_ITER> = 1 (Two mode profile segments, 1 OS then 1 SH, then not other profile)",
                                requirements = ["[L161_ETCS2-TRK_sSyRS_00684]"])

            sheet.ExpectedResult("SLR: Mode profile <D_MAMODE> / Iteration #1 = 0",
                                parameters= ["Route_Map/RM_operational_conditions_layer/MPs/MP/start_location/offset",
                                            "Route_Map/RM_operational_conditions_layer/MPs/MP/start_location/qdir",
                                            "Route_Map/RM_operational_conditions_layer/MPs/MP/start_location/segment_id",
                                            "Route_Map/RM_operational_conditions_layer/MPs/MP/end_location/offset",
                                            "Route_Map/RM_operational_conditions_layer/MPs/MP/end_location/qdir",                                            
                                            "Route_Map/RM_operational_conditions_layer/MPs/MP/SH_offset"])
            
            sheet.ExpectedResult("SLR: Mode profile <L_MAMODE> / Iteration #1 = <Referential/Route/MovementAuthorityPacket/DistanceLrbgToStartSignal> (OS up to start signal)",
                                requirements = ["[L161_ETCS2-TRK_sSyRS_00285]", 
                                                "[L161_ETCS2-TRK_sSyRS_00286]", 
                                                "[L161_ETCS2-TRK_sSyRS_00287]",
                                                "[L161_ETCS2-TRK_sSyRS_00309]"],
                                parameters= ["Route_Map/RM_operational_conditions_layer/MPs/MP/end_location/offset",
                                            "Route_Map/RM_operational_conditions_layer/MPs/MP/end_location/qdir",
                                            "Route_Map/RM_operational_conditions_layer/MPs/MP/end_location/segment_id"])
            
            sheet.ExpectedResult("SLR: Mode profile <M_MAMODE> / Iteration #1 = 0 (Onsight)",
                                parameters = ["Route_Map/RM_operational_conditions_layer/MPs/MP/mp_mode"])

            sheet.ExpectedResult("SLR: Mode profile <D_MAMODE> / Iteration #2 = <Referential/Route/MovementAuthorityPacket/DistanceLrbgToStartSignal> ",
                                requirements = ["[L161_ETCS2-TRK_sSyRS_00309]",
                                                "[L161_ETCS2-TRK_sSyRS_00264]",
                                                "[L161_ETCS2-TRK_sSyRS_00265]",
                                                "[L161_ETCS2-TRK_sSyRS_00682]"],
                                parameters= ["Route_Map/RM_operational_conditions_layer/MPs/MP/start_location/offset",
                                            "Route_Map/RM_operational_conditions_layer/MPs/MP/start_location/qdir",
                                            "Route_Map/RM_operational_conditions_layer/MPs/MP/start_location/segment_id"])
            
            sheet.ExpectedResult("SLR: Mode profile <L_MAMODE> / Iteration #2 = 32767 (Infinite) (SH from start signal with infinite distance)",
                                requirements = ["[L161_ETCS2-TRK_sSyRS_00285]", 
                                                "[L161_ETCS2-TRK_sSyRS_00286]", 
                                                "[L161_ETCS2-TRK_sSyRS_00287]",
                                                "[L161_ETCS2-TRK_sSyRS_00282]",
                                                "[L161_ETCS2-TRK_sSyRS_00682]",
                                                "[L161_ETCS2-TRK_sSyRS_00683]"],
                                parameters= ["Route_Map/RM_operational_conditions_layer/MPs/MP/end_location/offset",
                                            "Route_Map/RM_operational_conditions_layer/MPs/MP/end_location/qdir",
                                            "Route_Map/RM_operational_conditions_layer/MPs/MP/end_location/segment_id"])

            sheet.ExpectedResult("SLR: Mode profile <M_MAMODE> / Iteration #2 = 1 (Shunting)",
                                requirements = ["[L161_ETCS2-TRK_sSyRS_00282]"],
                                parameters = ["Route_Map/RM_operational_conditions_layer/MPs/MP/mp_mode"])
    
        # Checks for both OS and SH
        sheet.ExpectedResult("SLR: Mode profile <V_MAMODE> = 127 (Use national value)",
                            requirements = ["[L161_ETCS2-TRK_sSyRS_00283]"],
                            parameters = ["Route_Map/RM_operational_conditions_layer/MPs/MP/speed_level"])
        
        sheet.ExpectedResult("SLR: Mode profile <L_ACKMAMODE> = 150 (meters)",
                            requirements = ["[L161_ETCS2-TRK_sSyRS_00288]"],
                            parameters = ["Route_Map/RM_operational_conditions_layer/MPs/MP/acknowledgement_distance"])
        
        sheet.ExpectedResult("SLR: Mode profile <Q_MAMODE> = 1 (as both the EOA and SvL)",
                            requirements = ["[L161_ETCS2-TRK_sSyRS_00284]"],
                            parameters = ["Route_Map/RM_operational_conditions_layer/MPs/MP/MP_begin_supervision"])  
        
def ExpectedResultsDrivePastSignal(sheet, aspect:Aspects):
    if aspect == Aspects.PROCEED:
        sheet.ExpectedResult("SLR: Position Report with <M_MODE> = 0 (Full supervision)",
                              requirements = ["[L161_ETCS2-TRK_sSyRS_00170]",
                                              "[L161_ETCS2-TRK_sSyRS_00174]",
                                              "[L161_ETCS2-TRK_sSyRS_00268]"])
    if aspect == Aspects.RP:
        sheet.ExpectedResult("SLR: Position Report with <M_MODE> = 1 (Onsight)",
                              requirements = ["[L161_ETCS2-TRK_sSyRS_00175]"])
    elif aspect == Aspects.RW:
        sheet.ExpectedResult("SLR: Position Report with <M_MODE> = 3 (Shunting)",
                              requirements = ["[L161_ETCS2-TRK_sSyRS_00171]"])
        