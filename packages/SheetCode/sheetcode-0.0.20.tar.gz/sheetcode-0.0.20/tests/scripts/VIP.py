from SheetCode import Sheet
import scripts.RT_Common as RT_Common

sheet = Sheet(__file__)

sheet.Name = "Virtual information points"
sheet.Description = ["For each elementary route with one or more <Referential/Route/PlainTextMessagePacket>, check that text message associated to the VIP is sent to OBU",
                      "The start and end location will be checked along with other properties",
                      "This test shall be played with S-HMI in the test environment as it contributes to this function",
                      "=>S* for closed CVT signal inside the ETCS area: PX-V.8, CZ-W.8, OX-W.8, GZ-U.8, OZ-V.8, KX-U.8, NZ-W.8",
                      "=>S for closed VNS signal on the right in ETCS area: M5-V.8, M3-V.8, M1-V.8, L6-U.8, L4-U.8, L2-U.8",
                      "L<line> for closed CVT signal inside the ETCS area: to be checked with track plan, No deviation from generic rules for text message change of line in the project scope"]


sheet.StartConditions = ["No elementary routes is set or locked.",
                          "No train is set on the track."]

# *********************************************************************************************************************************************
sheet.Case("VIP")
RT_Common.InitialConditionsL2(sheet, RT_Common.Aspects.RNP, RT_Common.InitialPositions.Valid)

sheet.ExpectedResult("SLR: <Object_DYN_VIRTUAL_POINT/virtual_information_point/activation_status> = DISABLED")

sheet.Action(f"Set route under test in FS")

sheet.ExpectedResult("SLR: <Object_DYN_VIRTUAL_POINT/virtual_information_point/activation_status> = ENFORCED",
                        requirements = ["[L161_ETCS2-TRK_sSyRS_00473]",
                                        "[L161_ETCS2-TRK_sSyRS_00474]",
                                        "[L161_ETCS2-TRK_sSyRS_00475]",
                                        "[L161_ETCS2-TRK_sSyRS_00458]"],
                        parameters = ["LK/Output/Virtual information points/VIP_activation_enforced"])

sheet.ExpectedResult("SLR: Plain Text Message Packet 72 is sent to train",
                    requirements = ["[L161_ETCS2-TRK_sSyRS_00456]",
                                    "[L161_ETCS2-TRK_sSyRS_00459]",
                                    "[L161_ETCS2-TRK_sSyRS_00486]",
                                    "[L161_ETCS2-TRK_sSyRS_00487]",
                                    "[L161_ETCS2-TRK_sSyRS_00488]",
                                    "[L161_ETCS2-TRK_sSyRS_00489]"])

sheet.ExpectedResult("SLR: Plain Text Message <Q_TEXTCLASS> = 1 (Important Information)")

sheet.ExpectedResult("SLR: Plain Text Message <Q_TEXTDISPLAY> = 1 (Display as soon as / until all events are fulfilled)")
                                 
sheet.ExpectedResult("SLR: Plain Text Message <D_TEXTDISPLAY> = <Referential/Route/PlainTextMessagePacket/D_TEXTDISPLAY>",
                    requirements = ["[L161_ETCS2-TRK_sSyRS_00460]",
                                    "[L161_ETCS2-TRK_sSyRS_00461]",
                                    "[L161_ETCS2-TRK_sSyRS_00462]",
                                    "[L161_ETCS2-TRK_sSyRS_00463]",
                                    "[L161_ETCS2-TRK_sSyRS_00464]",
                                    "[L161_ETCS2-TRK_sSyRS_00465]",
                                    "[L161_ETCS2-TRK_sSyRS_00466]",
                                    "[L161_ETCS2-TRK_sSyRS_00467]",
                                    "[L161_ETCS2-TRK_sSyRS_00468]"],
                    parameters= ["Route_Map/RM_operational_conditions_layer/virtual_information_points/virtual_information_point/direction",
                                "Route_Map/RM_operational_conditions_layer/virtual_information_points/virtual_information_point/start_text_display_distance",
                                "Route_Map/RM_operational_conditions_layer/virtual_information_points/virtual_information_point/location/offset",
                                "Route_Map/RM_operational_conditions_layer/virtual_information_points/virtual_information_point/location/segment_id",
                                "Route_Map/RM_operational_conditions_layer/virtual_information_points/virtual_information_point/id",
                                "Route_Map/RM_operational_conditions_layer/virtual_information_points/virtual_information_point/VIP_type",
                                "Route_Map/RM_operational_conditions_layer/virtual_information_points/virtual_information_point/Vip_number"])

sheet.ExpectedResult("SLR: Plain Text Message <M_MODETEXTDISPLAY> = 15 (Not limited by mode)",
                    requirements = ["[L161_ETCS2-TRK_sSyRS_00476]"])

sheet.ExpectedResult("SLR: Plain Text Message <M_LEVELTEXTDISPLAY> = 5 (Not limited by level)")

sheet.ExpectedResult("SLR: Plain Text Message <L_TEXTDISPLAY> = <Referential/Route/PlainTextMessagePacket/L_TEXTDISPLAY>",
                    requirements = ["[L161_ETCS2-TRK_sSyRS_00450]",
                                    "[L161_ETCS2-TRK_sSyRS_00452]",
                                    "[L161_ETCS2-TRK_sSyRS_00469]",
                                    "[L161_ETCS2-TRK_sSyRS_00470]",
                                    "[L161_ETCS2-TRK_sSyRS_00471]"],
                    parameters= ["Route_Map/RM_operational_conditions_layer/virtual_information_points/virtual_information_point/direction",
                                "Route_Map/RM_operational_conditions_layer/virtual_information_points/virtual_information_point/end_text_display_distance",
                                "Route_Map/RM_operational_conditions_layer/virtual_information_points/virtual_information_point/location/offset",
                                "Route_Map/RM_operational_conditions_layer/virtual_information_points/virtual_information_point/location/segment_id"])

sheet.ExpectedResult("SLR: Plain Text Message <T_TEXTDISPLAY> = <Referential/Route/PlainTextMessagePacket/T_TEXTDISPLAY>",
                    requirements = ["[L161_ETCS2-TRK_sSyRS_00477]",
                                    "[L161_ETCS2-TRK_sSyRS_00478]",
                                    "[L161_ETCS2-TRK_sSyRS_00454]"])

sheet.ExpectedResult("SLR: Plain Text Message <M_MODETEXTDISPLAY2> = 15 (Not limited by mode)",
                    requirements = ["[L161_ETCS2-TRK_sSyRS_00479]"])

sheet.ExpectedResult("SLR: Plain Text Message <M_LEVELTEXTDISPLAY2> = 5 (Not limited by level)")

sheet.ExpectedResult("SLR: Plain Text Message <Q_TEXTCONFIRM> = <Referential/Route/PlainTextMessagePacket/Q_TEXTCONFIRM>",
                    requirements = ["[L161_ETCS2-TRK_sSyRS_00480]",
                                    "[L161_ETCS2-TRK_sSyRS_00481]"])

sheet.ExpectedResult("SLR: Plain Text Message <Q_CONFTEXTDISPLAY> = 0 (Driver acknowledgement always ends the text display)")

sheet.ExpectedResult("SLR: Plain Text Message <X_TEXT> = <Referential/Route/PlainTextMessagePacket/X_TEXT>",
                    requirements = ["[L161_ETCS2-TRK_sSyRS_00482]",
                                    "[L161_ETCS2-TRK_sSyRS_00483]",
                                    "[L161_ETCS2-TRK_sSyRS_00484]",
                                    "[L161_ETCS2-TRK_sSyRS_00485]",
                                    "[L161_ETCS2-TRK_sSyRS_00450]",
                                    "[L161_ETCS2-TRK_sSyRS_00452]",
                                    "[L161_ETCS2-TRK_sSyRS_00454]"])


sheet.Save()

