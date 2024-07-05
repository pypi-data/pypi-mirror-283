from SheetCode import Sheet
sheet = Sheet(__file__)

sheet.Name = "Inspection of RBC Static XML"
sheet.Description =["Inspection of parameter values in RBC Datapreparation."
                    "Whenever possible, a functional tests is performed through other test sheets.",
                    "When not possible, an inspection of the parameter value is realized.",
                    "Also, we check that parameters related to unused functions are set to default values and to 'N_of' parameters are set to 0."]

sheet.StartConditions = ["n.a."]

# ---------------------------------------------------------------------------------------------------------------------------------------------
sheet.Case("Miscellaneous parameters")

sheet.Action("Inspect RBC static.xml")
sheet.ExpectedResult("Nmax_n_iter_packet_21 = 31",
                    requirements = ["[L161_ETCS2-TRK_sSyRS_00678]"],
                    parameters = ["Customization_Data/RBC_configuration_layer/sizing_parameters/Nmax_n_iter_packet_21"])
sheet.ExpectedResult("Nmax_n_iter_packet_27 = 31",
                    requirements = ["[L161_ETCS2-TRK_sSyRS_00255]"],
                    parameters = ["Customization_Data/RBC_configuration_layer/sizing_parameters/Nmax_n_iter_packet_27"])
sheet.ExpectedResult("Nmax_n_iter = Nmax_n_iter_packet_27 + 1 = 28",
                    requirements = ["[L161_ETCS2-TRK_sSyRS_00259]"],
                    parameters = ["Customization_Data/RBC_configuration_layer/sizing_parameters/Nmax_n_iter"])
sheet.ExpectedResult("MA_sending_on_path_extension = TRUE",
                    requirements = ["[L161_ETCS2-TRK_sSyRS_00271]"],
                    parameters = ["Customization_Data/RBC_configuration_layer/ERTMS_system_parameters/MA_sending_on_path_extension"])
sheet.ExpectedResult("path_extension_on_MA_request = FALSE",
                    requirements = ["[L161_ETCS2-TRK_sSyRS_00272]"],
                    parameters = ["Customization_Data/RBC_configuration_layer/ERTMS_system_parameters/path_extension_on_MA_request"])
sheet.ExpectedResult("path_extend_only_when_position_report_validated = TRUE",
                    requirements = ["[L161_ETCS2-TRK_sSyRS_00273]"],
                    parameters = ["Customization_Data/RBC_configuration_layer/ERTMS_system_parameters/Path_Extend_Only_When_Position_Report_Validated"])
sheet.ExpectedResult("Nmax_path_blocks = 5",
                    requirements = ["[L161_ETCS2-TRK_sSyRS_00274]"],
                    parameters = ["Customization_Data/RBC_configuration_layer/ERTMS_system_parameters/Nmax_path_blocks"])
sheet.ExpectedResult("track_occupation_available = TRUE",
                    requirements = ["[L161_ETCS2-TRK_sSyRS_00275]"],
                    parameters = ["Customization_Data/RBC_configuration_layer/ERTMS_system_parameters/track_occupation_available"])
sheet.ExpectedResult("use_proximity_window_for_permissive_block = TRUE",
                    requirements = ["[L161_ETCS2-TRK_sSyRS_00278]",
                                    "[L161_ETCS2-TRK_sSyRS_00688]"],
                    parameters = ["Customization_Data/RBC_configuration_layer/ERTMS_system_parameters/use_proximity_window_for_permissive_block"])
sheet.ExpectedResult("start_on_new_balise_group = TRUE for all PBG (Point Balise Groups)",
                    requirements = ["[L161_ETCS2-TRK_sSyRS_00365]"],
                    parameters = ["Route_Map/RM_RTM_layer/balise_groups/balise_group/start_on_new_balise_group"])
sheet.ExpectedResult("ignore_cnn_locking_under_train = TRUE",
                    requirements = ["[L161_ETCS2-TRK_sSyRS_00687]"],
                    parameters = ["Customization_Data/RBC_configuration_layer/ERTMS_system_parameters/ignore_cnn_locking_under_train"])
sheet.ExpectedResult("For all Mode Profiles, MP_activation_status = DISABLED",
                    parameters = ["Route_Map/RM_operational_conditions_layer/MPs/MP/MP_activation_status"])
sheet.ExpectedResult("min_track_ahead_free_distance = max_track_ahead_free_distance = 150 m, for all main stopping point connections, except for L1 S3, L2 S1 and the signal leading to L2 S1",
                    requirements = ["[L161_ETCS2-TRK_sSyRS_00146]",
                                    "[L161_ETCS2-TRK_sSyRS_00147]"],
                    parameters = ["Route_Map/RM_interlocking_layer/TAF_windows/TAF_window/min_track_ahead_free_distance",
                                  "Route_Map/RM_interlocking_layer/TAF_windows/TAF_window/max_track_ahead_free_distance"])
sheet.ExpectedResult("min_track_ahead_free_distance = max_track_ahead_free_distance = 0 m, for main stopping point connections associated to L1 S3, L2 S1 and the signal leading to L2 S1",
                    requirements = ["[L161_ETCS2-TRK_sSyRS_00146]",
                                    "[L161_ETCS2-TRK_sSyRS_00148]"],
                    parameters = ["Route_Map/RM_interlocking_layer/TAF_windows/TAF_window/min_track_ahead_free_distance",
                                  "Route_Map/RM_interlocking_layer/TAF_windows/TAF_window/max_track_ahead_free_distance"])
sheet.ExpectedResult("ATAF_allowed = TRUE for all main stoppng point connection, except for L1 S3, L2 S1 and the signal leading to L2 S1",
                    requirements = ["[L161_ETCS2-TRK_sSyRS_00149]"],
                    parameters = ["Route_Map/RM_interlocking_layer/TAF_windows/TAF_window/ATAF_allowed"])
sheet.ExpectedResult("TAF_request_only_for_SB_PT_train_in_TAF_window = FALSE",
                    requirements = ["[L161_ETCS2-TRK_sSyRS_00151]"],
                    parameters = ["Customization_Data/RBC_configuration_layer/ERTMS_system_parameters/TAF_request_only_for_SB_PT_train_in_TAF_window"])
sheet.ExpectedResult("CES_ignored_if_entering_train = FALSE for all main stopping point connection",
                    requirements = ["[L161_ETCS2-TRK_sSyRS_00580]"],
                    parameters = ["Route_Map/RM_interlocking_layer/connections/connection/CES_ignored_if_entering_train"])
sheet.ExpectedResult("Nmax_RBC_suitability_parameter = 1 (One area only)",
                    requirements = ["[L161_ETCS2-TRK_sSyRS_00084]",
                                    "[L161_ETCS2-TRK_sSyRS_00085]"],
                    parameters = ["Customization_Data/RBC_configuration_layer/RBC_suitability_parameters/Nmax_RBC_suitability_parameter"])
sheet.ExpectedResult("There is only one instance of RBC_global_suitability_parameter_id",
                    requirements = ["[L161_ETCS2-TRK_sSyRS_00085]"],
                    parameters = ["Customization_Data/RBC_configuration_layer/ERTMS_system_parameters/RBC_global_suitability_parameter_id"])
sheet.ExpectedResult("minimum_train_length = 0 (To allow all trains)",
                    requirements = ["[L161_ETCS2-TRK_sSyRS_00086]"],
                    parameters = ["Customization_Data/RBC_configuration_layer/RBC_suitability_parameters/RBC_suitability_parameter/minimum_train_length"])
sheet.ExpectedResult("maximum_train_length = 4095 (To allow all trains)",
                    requirements = ["[L161_ETCS2-TRK_sSyRS_00086]"],
                    parameters = ["Customization_Data/RBC_configuration_layer/RBC_suitability_parameters/RBC_suitability_parameter/maximum_train_length"])
sheet.ExpectedResult("minimum_train_speed = 0 (To allow all trains)",
                    requirements = ["[L161_ETCS2-TRK_sSyRS_00086]"],
                    parameters = ["Customization_Data/RBC_configuration_layer/RBC_suitability_parameters/RBC_suitability_parameter/minimum_train_speed"])
sheet.ExpectedResult("maximum_train_speed = 600 (To allow all trains)",
                    requirements = ["[L161_ETCS2-TRK_sSyRS_00086]"],
                    parameters = ["Customization_Data/RBC_configuration_layer/RBC_suitability_parameters/RBC_suitability_parameter/maximum_train_speed"])
sheet.ExpectedResult("Nmax_axleload_value = 0 (To allow all trains)",
                    requirements = ["[L161_ETCS2-TRK_sSyRS_00087]"],
                    parameters = ["Customization_Data/RBC_configuration_layer/RBC_suitability_parameters/RBC_suitability_parameter/axleload_values/Nmax_axleload_value"])
sheet.ExpectedResult("Nmax_loadinggauge = 0 (To allow all trains)",
                    requirements = ["[L161_ETCS2-TRK_sSyRS_00088]"],
                    parameters = ["Customization_Data/RBC_configuration_layer/RBC_suitability_parameters/RBC_suitability_parameter/loadinggauges/Nmax_loadinggauge"])
sheet.ExpectedResult("Nmax_traction_type = 0 (To allow all trains)",
                    requirements = ["[L161_ETCS2-TRK_sSyRS_00089]"],
                    parameters = ["Customization_Data/RBC_configuration_layer/RBC_suitability_parameters/RBC_suitability_parameter/traction_list/Nmax_traction_type"])
sheet.ExpectedResult("Nmax_suitability_train_category = 0 (To allow all trains)",
                    requirements = ["[L161_ETCS2-TRK_sSyRS_00090]"],
                    parameters = ["Customization_Data/RBC_configuration_layer/RBC_suitability_parameters/RBC_suitability_parameter/train_categories/Nmax_suitability_train_category"])
sheet.ExpectedResult("send_SR_authorisation_only_if_next_block_available = FALSE",
                    requirements = ["[L161_ETCS2-TRK_sSyRS_00101]",
                                    "[L161_ETCS2-TRK_sSyRS_00113]"],
                    parameters = ["Customization_Data/RBC_configuration_layer/ERTMS_system_parameters/send_SR_authorisation_only_if_next_block_available"])
sheet.ExpectedResult("Inhibit_SR_authorisation_in_TAF = FALSE",
                    requirements = ["[L161_ETCS2-TRK_sSyRS_00101]"],
                    parameters = ["Customization_Data/RBC_configuration_layer/ERTMS_system_parameters/Inhibit_SR_authorisation_in_TAF"])
sheet.ExpectedResult("send_SR_authorisation_to_unlocalised_train_only = FALSE",
                    requirements = ["[L161_ETCS2-TRK_sSyRS_00102]"],
                    parameters = ["Customization_Data/RBC_configuration_layer/ERTMS_system_parameters/send_SR_authorisation_to_unlocalised_train_only"])
sheet.ExpectedResult("start_on_new_balise_group = TRUE for all PBG (Point BG).\nNote: PBG NID_C/NID_BG are extracted from document DAA-000029 'Balise locations'",
                    requirements = ["[L161_ETCS2-TRK_sSyRS_00104]"],
                    parameters = ["Route_Map/RM_RTM_layer/balise_groups/balise_group/start_on_new_balise_group"])
sheet.ExpectedResult("text_message_following_SOM_when_no_path = FALSE",
                    requirements = ["[L161_ETCS2-TRK_sSyRS_00114]"],
                    parameters = ["Customization_Data/RBC_configuration_layer/ERTMS_system_parameters/text_message_following_SOM_when_no_path"])
sheet.ExpectedResult("text_message_following_SoM_when_no_path_id = 0 (Not defined)",
                    requirements = ["[L161_ETCS2-TRK_sSyRS_00114]"],
                    parameters = ["Customization_Data/RBC_configuration_layer/ERTMS_system_parameters/text_message_following_SOM_when_no_path_id"])
sheet.ExpectedResult("TAF_allowed_at_path_end = FALSE (All instances)",
                    requirements = ["[L161_ETCS2-TRK_sSyRS_00123]"],
                    parameters = ["Route_Map/RM_interlocking_layer/TAF_windows/TAF_window/TAF_allowed_at_path_end"])
sheet.ExpectedResult("UES_in_mute_if_emergency = FALSE",
                    requirements = ["[L161_ETCS2-TRK_sSyRS_00154]"],
                    parameters = ["Route_Map/RM_interlocking_layer/connections/connection/UES_in_mute_if_emergency"])
sheet.ExpectedResult("UES_in_mute_if_emergency_marker = FALSE",
                    requirements = ["[L161_ETCS2-TRK_sSyRS_00154]"],
                    parameters = ["Customization_Data/RBC_configuration_layer/ERTMS_system_parameters/UES_in_mute_if_emergency_marker"])
sheet.ExpectedResult("OS_SH_authorisation_allowed = FALSE (for all connections)",
                    requirements = ["[L161_ETCS2-TRK_sSyRS_00155]"],
                    parameters = ["Route_Map/RM_interlocking_layer/connections/connection/OS_SH_authorisation_allowed"])
sheet.ExpectedResult("send_OS_SH_authorisation_only_if_next_block_available = FALSE",
                    requirements = ["[L161_ETCS2-TRK_sSyRS_00156]"],
                    parameters = ["Customization_Data/RBC_configuration_layer/ERTMS_system_parameters/send_OS_SH_authorisation_only_if_next_block_available"])
sheet.ExpectedResult("prevent_OS_SH_MA_author_when_connected_train = FALSE",
                    requirements = ["[L161_ETCS2-TRK_sSyRS_00157]"],
                    parameters = ["Customization_Data/RBC_configuration_layer/ERTMS_system_parameters/prevent_OS_SH_MA_author_when_connected_train"])
sheet.ExpectedResult("send_UES_for_reconnected_train_in_FS_LS_OS = FALSE",
                    requirements = ["[L161_ETCS2-TRK_sSyRS_00159]"],
                    parameters = ["Customization_Data/RBC_configuration_layer/ERTMS_system_parameters/send_UES_for_reconnected_train_in_FS_LS_OS"])
sheet.ExpectedResult("UES_from_ED_creation_allowed_in_override = TRUE",
                    requirements = ["[L161_ETCS2-TRK_sSyRS_00224]"],
                    parameters = ["Customization_Data/RBC_configuration_layer/ERTMS_system_parameters/UES_from_ED_creation_allowed_in_override"])
sheet.ExpectedResult("override_ED_timer = 0",
                    requirements = ["[L161_ETCS2-TRK_sSyRS_00224]"],
                    parameters = ["Customization_Data/RBC_configuration_layer/timers/override_ED_timer"])
sheet.ExpectedResult("resend_UES_when_SR_entered = TRUE",
                    requirements = ["[L161_ETCS2-TRK_sSyRS_00230]"],
                    parameters = ["Customization_Data/RBC_configuration_layer/ERTMS_system_parameters/resend_UES_when_SR_entered"])
sheet.ExpectedResult("proximity_window/d_start = 150 meters (for all instances)",
                    requirements = ["[L161_ETCS2-TRK_sSyRS_00279]"],
                    parameters = ["Route_Map/RM_interlocking_layer/stopping_points/stopping_point/proximity_window/d_start"])
sheet.ExpectedResult("proximity_window/maximum_speed = 30 km/h (for all instances)",
                    requirements = ["[L161_ETCS2-TRK_sSyRS_00279]"],
                    parameters = ["Route_Map/RM_interlocking_layer/stopping_points/stopping_point/proximity_window/maximum_speed"])
sheet.ExpectedResult("v_OS_activation = 605 (IRRELEVANT, for all instances)",
                    requirements = ["[L161_ETCS2-TRK_sSyRS_00289]"],
                    parameters = ["Route_Map/RM_operational_conditions_layer/MPs/MP/v_OS_activation"])
sheet.ExpectedResult("l_OS_activation = 327670 (IRRELEVANT, for all instances)",
                    requirements = ["[L161_ETCS2-TRK_sSyRS_00289]"],
                    parameters = ["Route_Map/RM_operational_conditions_layer/MPs/MP/l_OS_activation"])
sheet.ExpectedResult("OS_autoactivation_type = NONE (for all instances)",
                    requirements = ["[L161_ETCS2-TRK_sSyRS_00289]"],
                    parameters = ["Route_Map/RM_operational_conditions_layer/MPs/MP/OS_autoactivation_type"])
sheet.ExpectedResult("OS_train_only = FALSE (for all instances)",
                    requirements = ["[L161_ETCS2-TRK_sSyRS_00290]"],
                    parameters = ["Route_Map/RM_operational_conditions_layer/MPs/MP/OS_train_only"])
sheet.ExpectedResult("upgrade_window_application = NOT_APPLICABLE (for all instances)",
                    requirements = ["[L161_ETCS2-TRK_sSyRS_00291]"],
                    parameters = ["Route_Map/RM_operational_conditions_layer/MPs/MP/upgrade_window_application"])
sheet.ExpectedResult("upgrade_window_length = 0 (for all instances)",
                    requirements = ["[L161_ETCS2-TRK_sSyRS_00291]"],
                    parameters = ["Route_Map/RM_operational_conditions_layer/MPs/MP/upgrade_window_length"])
sheet.ExpectedResult("SH_offset = 0 (for all instances)",
                    requirements = ["[L161_ETCS2-TRK_sSyRS_00291]"],
                    parameters = ["Route_Map/RM_operational_conditions_layer/MPs/MP/SH_offset"])
sheet.ExpectedResult("Nmax_n_iter_packet_5 = 29",
                    requirements = ["[L161_ETCS2-TRK_sSyRS_00379]"],
                    parameters = ["Customization_Data/RBC_configuration_layer/sizing_parameters/Nmax_n_iter_packet_5"])
sheet.ExpectedResult("add_TSR_to_SSP = FALSE",
                    requirements = ["[L161_ETCS2-TRK_sSyRS_00397]"],
                    parameters = ["Route_Map/RM_operational_conditions_layer/TSRs/TSR/add_TSR_to_SSP"])
sheet.ExpectedResult("TSR_Text_Display_Distance_Upstream = 0 meters",
                    requirements = ["[L161_ETCS2-TRK_sSyRS_00398]"],
                    parameters = ["Customization_Data/RBC_configuration_layer/ERTMS_system_parameters/TSR_Text_Display_Distance_Upstream"])
sheet.ExpectedResult("TSR_Text_Display_Distance_Downstream = 0 meters",
                    requirements = ["[L161_ETCS2-TRK_sSyRS_00398]"],
                    parameters = ["Customization_Data/RBC_configuration_layer/ERTMS_system_parameters/TSR_Text_Display_Distance_Downstream"])
sheet.ExpectedResult("NV_with_pos_rep_after_SR_author = TRUE",
                    requirements = ["[L161_ETCS2-TRK_sSyRS_00437]"],
                    parameters = ["Customization_Data/RBC_configuration_layer/ERTMS_system_parameters/NV_with_pos_rep_after_SR_author"])
sheet.ExpectedResult("pos_rep_after_SR_author = TRUE",
                    requirements = ["[L161_ETCS2-TRK_sSyRS_00437]"],
                    parameters = ["Customization_Data/RBC_configuration_layer/ERTMS_system_parameters/pos_rep_after_SR_author"])
sheet.ExpectedResult("Send_PR_params_after_Train_Data = TRUE",
                    requirements = ["[L161_ETCS2-TRK_sSyRS_00439]"],
                    parameters = ["Customization_Data/RBC_configuration_layer/ERTMS_system_parameters/send_PR_params_after_train_data"])
sheet.ExpectedResult("NV_with_pos_rep_after_SR_author = TRUE",
                    requirements = ["[L161_ETCS2-TRK_sSyRS_00440]"],
                    parameters = ["Customization_Data/RBC_configuration_layer/ERTMS_system_parameters/NV_with_pos_rep_after_SR_author"])
sheet.ExpectedResult("disconnect_not_authorised_train = FALSE",
                    requirements = ["[L161_ETCS2-TRK_sSyRS_00644]"],
                    parameters = ["Customization_Data/RBC_configuration_layer/ERTMS_system_parameters/disconnect_not_authorised_train"])
sheet.ExpectedResult("Disconnection_and_text_when_train_data_KO = FALSE",
                    requirements = ["[L161_ETCS2-TRK_sSyRS_00645]"],
                    parameters = ["Customization_Data/RBC_configuration_layer/ERTMS_system_parameters/Disconnection_and_text_when_train_data_KO"])
sheet.ExpectedResult("disconnect_NL_trains = FALSE",
                    requirements = ["[L161_ETCS2-TRK_sSyRS_00646]"],
                    parameters = ["Customization_Data/RBC_configuration_layer/ERTMS_system_parameters/disconnect_NL_trains"])
sheet.ExpectedResult("check_train_data_received_timer = 0",
                    requirements = ["[L161_ETCS2-TRK_sSyRS_00649]"],
                    parameters = ["Customization_Data/RBC_configuration_layer/timers/check_train_data_received_timer"])
sheet.ExpectedResult("disconnection_and_text_when_odometry_error_too_high = FALSE",
                    requirements = ["[L161_ETCS2-TRK_sSyRS_00650]"],
                    parameters = ["Customization_Data/RBC_configuration_layer/ERTMS_system_parameters/disconnection_and_text_when_odometry_error_too_high"])
sheet.ExpectedResult("check_train_position_lost = FALSE",
                    requirements = ["[L161_ETCS2-TRK_sSyRS_00658]"],
                    parameters = ["Customization_Data/RBC_configuration_layer/ERTMS_system_parameters/check_train_position_lost"])
sheet.ExpectedResult("position_report_timer = 2592000",
                    requirements = ["[L161_ETCS2-TRK_sSyRS_00658]"],
                    parameters = ["Customization_Data/RBC_configuration_layer/timers/position_report_timer"])
sheet.ExpectedResult("Mute_timer = 180 seconds (same as MW's mobile_timeout_duration_EVC)",
                    requirements = ["[L161_ETCS2-TRK_sSyRS_00662]"],
                    parameters = ["Customization_Data/RBC_configuration_layer/timers/mute_timer"])
sheet.ExpectedResult("Train_disconnection_timer = 300 seconds",
                    requirements = ["[L161_ETCS2-TRK_sSyRS_00663]"],
                    parameters = ["Customization_Data/RBC_configuration_layer/timers/Train_disconnection_timer"])
sheet.ExpectedResult("Reception_timer = 481 seconds",
                    requirements = ["[L161_ETCS2-TRK_sSyRS_00664]"],
                    parameters = ["Customization_Data/RBC_configuration_layer/timers/reception_timer"])
sheet.ExpectedResult("TAF_granted_response_time = 0 seconds",
                    requirements = ["[L161_ETCS2-TRK_sSyRS_00667]"],
                    parameters = ["Customization_Data/RBC_configuration_layer/timers/TAF_granted_response_time"])
sheet.ExpectedResult("specific_train_TSR_allowed = FALSE",
                    requirements = ["[L161_ETCS2-TRK_sSyRS_00668]"],
                    parameters = ["Customization_Data/RBC_configuration_layer/ERTMS_system_parameters/specific_train_TSR_allowed"])
sheet.ExpectedResult("train_category_TSR_allowed = FALSE",
                    requirements = ["[L161_ETCS2-TRK_sSyRS_00669]"],
                    parameters = ["Customization_Data/RBC_configuration_layer/ERTMS_system_parameters/train_category_TSR_allowed"])
sheet.ExpectedResult("TSR_From_LCS_Always_Not_Revokable = FALSE",
                    requirements = ["[L161_ETCS2-TRK_sSyRS_00670]"],
                    parameters = ["Customization_Data/RBC_configuration_layer/ERTMS_system_parameters/Tsr_From_LCS_always_Not_Revokable"])
sheet.ExpectedResult("use_RBC_LK = TRUE",
                    requirements = ["[L161_ETCS2-TRK_sSyRS_00694]"],
                    parameters = ["Customization_Data/RBC_configuration_layer/ERTMS_system_parameters/use_RBC_LK"])
sheet.ExpectedResult("check_train_btwn_front_end_eos = TRUE",
                    requirements = ["[L161_ETCS2-TRK_sSyRS_00698]"],
                    parameters = ["Customization_Data/RBC_configuration_layer/ERTMS_system_parameters/Check_train_btwn_front_end_eos"])
sheet.ExpectedResult("check_connected_train_from_min_to_max_front = FALSE",
                    requirements = ["[L161_ETCS2-TRK_sSyRS_00699]"],
                    parameters = ["Customization_Data/RBC_configuration_layer/ERTMS_system_parameters/check_connected_train_from_min_to_max_front"])
sheet.ExpectedResult("Nmax_train = 60 (as per SyPD)",
                    requirements = ["[L161_ETCS2-TRK_sSyRS_00711]",
                                    "[L161_ETCS2-TRK_sSyRS_00712]"],
                    parameters = ["Customization_Data/RBC_configuration_layer/sizing_parameters/Nmax_train"])
# ---------------------------------------------------------------------------------------------------------------------------------------------
sheet.Case("Entry boundaries")

sheet.Action("Inspect RBC static.xml")
sheet.ExpectedResult("Each BG-A and BG-A' is defined as an instance of <entry_balise_group/id>",
                    requirements = ["[L161_ETCS2-TRK_sSyRS_00515]"],
                    parameters = ["Route_Map/RM_RTM_layer/balise_groups/entry_balise_group/id"])
sheet.ExpectedResult("Each BG-A' is defined as an instance of <balise_group/id>",
                    requirements = ["[L161_ETCS2-TRK_sSyRS_00516]"],
                    parameters = ["Route_Map/RM_RTM_layer/balise_groups/balise_group/id"])
sheet.ExpectedResult("A buffer stop is placed on the single node upstream of each L2 entry boundary",
                    requirements = ["[L161_ETCS2-TRK_sSyRS_00517]"],
                    parameters = ["Route_Map/RM_civil_characteristics_layer/buffer_stops/buffer_stop/location/offset",
                                  "Route_Map/RM_civil_characteristics_layer/buffer_stops/buffer_stop/location/segment_id"])
sheet.ExpectedResult("Each BG located between BG-A' and the L2 entry border is defined as an instance of <balise_group/id>",
                    requirements = ["[L161_ETCS2-TRK_sSyRS_00520]"],
                    parameters = ["Route_Map/RM_RTM_layer/balise_groups/balise_group/id"])
sheet.ExpectedResult("Not point is located between BG-A and the L2 entry boundary, meaning that <Referential/Route/Points> is empty",
                    requirements = ["[L161_ETCS2-TRK_sSyRS_00521]"])
sheet.ExpectedResult("The BG-A and BG-A' associated to each boundary are not associated to another boundary",
                    requirements = ["[L161_ETCS2-TRK_sSyRS_00522]",
                                    "[L161_ETCS2-TRK_sSyRS_00523]"])
sheet.ExpectedResult("All instances of <entry_balise_group/v_min> = 0",
                    requirements = ["[L161_ETCS2-TRK_sSyRS_00524]"],
                    parameters = ["Route_Map/RM_RTM_layer/balise_groups/entry_balise_group/v_min"])
sheet.ExpectedResult("<Packet_41_to_Entering_Train> = TRUE",
                    requirements = ["[L161_ETCS2-TRK_sSyRS_00526]"],
                    parameters = ["Customization_Data/RBC_configuration_layer/ERTMS_system_parameters/Packet_41_to_Entering_Train"])
sheet.ExpectedResult("All instances of <boundary/packet_9_used> = FALSE",
                    requirements = ["[L161_ETCS2-TRK_sSyRS_00530]"],
                    parameters = ["Route_Map/RM_RTM_layer/boundaries/boundary/packet_9_used"])
sheet.ExpectedResult("No instance of <boundary/cancel_boundary_identity> exists",
                    requirements = ["[L161_ETCS2-TRK_sSyRS_00531]"],
                    parameters = ["Route_Map/RM_RTM_layer/boundaries/boundary/cancel_boundary_identity"])
sheet.ExpectedResult("<additional_conditions_to_cancel_entry> = FALSE",
                    requirements = ["[L161_ETCS2-TRK_sSyRS_00532]"],
                    parameters = ["Customization_Data/RBC_configuration_layer/ERTMS_system_parameters/additional_conditions_to_cancel_entry"])
sheet.ExpectedResult("<boundary/location> for entries are located exactly at the BG-T / N_PIG=0 location",
                    requirements = ["[L161_ETCS2-TRK_sSyRS_00537]"],
                    parameters = ["Route_Map/RM_RTM_layer/boundaries/boundary/location/offset",
                                  "Route_Map/RM_RTM_layer/boundaries/boundary/location/segment_id"])
sheet.ExpectedResult("Each BG-T is defined as an instance of <boundary/border_balise_group_id>",
                    requirements = ["[L161_ETCS2-TRK_sSyRS_00538]"],
                    parameters = ["Route_Map/RM_RTM_layer/boundaries/boundary/border_balise_group_id"])
sheet.ExpectedResult("Each entry boundary has <boundary_activation_status> = ENFORCED",
                    requirements = ["[L161_ETCS2-TRK_sSyRS_00546]"],
                    parameters = ["Route_Map/RM_RTM_layer/boundaries/boundary/boundary_activation_status"])
sheet.ExpectedResult("Outside responsibility profile is defined between each upstream single node and L2 boundary")
sheet.ExpectedResult("For each Outside responsibility profile <leaving_RBC_area> = FALSE",
                    requirements = ["[L161_ETCS2-TRK_sSyRS_00547]"],
                    parameters = ["Route_Map/RM_RTM_layer/Outside_Responsibility_Profiles/Outside_Responsibility_Profile/leaving_RBC_area"])
sheet.ExpectedResult("<enhanced_ambiguous_resolution> = TRUE",
                    requirements = ["[L161_ETCS2-TRK_sSyRS_00552]"],
                    parameters = ["Customization_Data/RBC_configuration_layer/ERTMS_system_parameters/enhanced_ambiguous_resolution"])
sheet.ExpectedResult("<ignore_cnn_locking_under_train> = TRUE",
                    requirements = ["[L161_ETCS2-TRK_sSyRS_00553]"],
                    parameters = ["Customization_Data/RBC_configuration_layer/ERTMS_system_parameters/ignore_cnn_locking_under_train"])
sheet.ExpectedResult("<check_point_position_for_path_creation> = FALSE",
                    requirements = ["[L161_ETCS2-TRK_sSyRS_00554]"],
                    parameters = ["Customization_Data/RBC_configuration_layer/ERTMS_system_parameters/check_point_position_for_path_creation"])


# ---------------------------------------------------------------------------------------------------------------------------------------------
sheet.Case("Exit boundaries")

sheet.Action("Inspect RBC static.xml")
sheet.ExpectedResult("No exit boundaries are defined. Meaning no instance of boundary/boundary_type> = ENTRY",
                    requirements = ["[L161_ETCS2-TRK_sSyRS_00593]"],
                    parameters = ["Route_Map/RM_RTM_layer/boundaries/boundary/boundary_type"])
sheet.ExpectedResult("train_disconnection_on_lower_level_transition = TRUE",
                    requirements = ["[L161_ETCS2-TRK_sSyRS_00585]"],
                    parameters = ["Customization_Data/RBC_configuration_layer/ERTMS_system_parameters/train_disconnection_on_lower_level_transition"])
sheet.ExpectedResult("A buffer stop is placed 2 meters downstream of the location of each L1 S3 signal",
                    requirements = ["[L161_ETCS2-TRK_sSyRS_00594]",
                                    "[L161_ETCS2-TRK_sSyRS_00595]",
                                    "[L161_ETCS2-TRK_sSyRS_00596]",
                                    "[L161_ETCS2-TRK_sSyRS_00599]"],
                    parameters = ["Route_Map/RM_civil_characteristics_layer/buffer_stops/buffer_stop/location/offset",
                                  "Route_Map/RM_civil_characteristics_layer/buffer_stops/buffer_stop/location/segment_id"])
sheet.ExpectedResult("The stopping point and danger points associated to each L1 S3 signal is located exactly at the signal",
                    requirements = ["[L161_ETCS2-TRK_sSyRS_00597]"])
sheet.ExpectedResult("For the connection associated to each L1 S3 signal, Route_Map/RM_interlocking_layer/connections/connection/locking_status = UNLOCKED",
                    requirements = ["[L161_ETCS2-TRK_sSyRS_00598]"])

# ---------------------------------------------------------------------------------------------------------------------------------------------
sheet.Case("Inspection of RBC parameters linked to VIP")

sheet.Action("Inspect RBC static.xml")

sheet.ExpectedResult("<Nmax_virtual_information_point> = Count of <Referential/Route/PlainTextMessagePacket>",
                    parameters = ["Route_Map/RM_operational_conditions_layer/virtual_information_points/Nmax_virtual_information_point"])
sheet.ExpectedResult("<virtual_information_point/VIP_applicability> = ALL_TRAINS", 
                    requirements = ["[L161_ETCS2-TRK_sSyRS_00487]",
                                    "[L161_ETCS2-TRK_sSyRS_00472]"],
                    parameters = ["Route_Map/RM_operational_conditions_layer/virtual_information_points/virtual_information_point/VIP_applicability"])
sheet.ExpectedResult("<virtual_information_point/activation_status> = DISABLED (by default)",
                    parameters = ["Route_Map/RM_operational_conditions_layer/virtual_information_points/virtual_information_point/activation_status"])
sheet.ExpectedResult("<virtual_information_point/N_VIP_train_category> = 0",
                    parameters = ["Route_Map/RM_operational_conditions_layer/virtual_information_points/virtual_information_point/N_VIP_train_category"])

# ---------------------------------------------------------------------------------------------------------------------------------------------
sheet.Case("Inspection of RBC parameters linked to Emergency detectors")

sheet.Action("Inspect RBC static.xml")

sheet.ExpectedResult("For each non-controlled main stop signal including L1S1 and L1S2, but excluding L2S1, a Emergency detector is set at the signal location in the route direction.",
                    requirements = ["[L161_ETCS2-TRK_sSyRS_00196]"],
                    parameters = ["Route_Map/RM_operational_conditions_layer/emergency_detectors/emergency_detector/location/offset",
                                  "Route_Map/RM_operational_conditions_layer/emergency_detectors/emergency_detector/location/segment_id"])

sheet.ExpectedResult("<emergency_detector/only_applicable_to_electric_train> = FALSE", 
                    parameters = [ "Route_Map/RM_operational_conditions_layer/emergency_detectors/emergency_detector/only_applicable_to_electric_train"])

sheet.ExpectedResult("<emergency_detector/Nmax_emergency_detector> = Count of <Referential/Route/EmergencyDetectors>", 
                    parameters = ["Route_Map/RM_operational_conditions_layer/emergency_detectors/Nmax_emergency_detector"])

# ---------------------------------------------------------------------------------------------------------------------------------------------
sheet.Case("Inspection of RBC parameters linked to Start of Mission")

sheet.Action("Inspect RBC static.xml")

sheet.ExpectedResult("<shunting_request_always_accepted> = TRUE",
                    requirements = ["[L161_ETCS2-TRK_sSyRS_00107]"],
                    parameters = ["Customization_Data/RBC_configuration_layer/ERTMS_system_parameters/shunting_request_always_accepted"])

# ---------------------------------------------------------------------------------------------------------------------------------------------
sheet.Case("Unused functions")

sheet.Save()