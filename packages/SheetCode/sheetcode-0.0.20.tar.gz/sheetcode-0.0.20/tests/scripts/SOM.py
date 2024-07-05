from SheetCode import Sheet

sheet = Sheet(__file__)

sheet.Name = "Start of Mission"
sheet.Description =["TBD"]

sheet.StartConditions = ["Awakening train"]

signalWithRnp = "DT8"
signalWithRp = "BX114"

# *********************************************************************************************************************************************
sheet.Case("SoM in L2 with a VALID position upstream of a controlled signal showing RNP aspect")
# ---------------------------------------------------------------------------------------------------------------------------------------------
sheet.Action(f"Set a train upstream of signal {signalWithRnp} showing RNP reporting on SBG and perform SoM in L2 with a VALID position")
sheet.ExpectedResult("Session is being established between EONBE and RBC")
# ---------------------------------------------------------------------------------------------------------------------------------------------
sheet.Action("SLR: Inspect SoM Position Report Message 157")
sheet.ExpectedResult("<NID_LRBG> = <Referential/Route/LRBG>")
sheet.ExpectedResult("<Q_STATUS> = 1 (Valid)")
# ---------------------------------------------------------------------------------------------------------------------------------------------
sheet.Action("SLR: Inspect System Version Message 32")
sheet.ExpectedResult("<M_VERSION> = 16 (1.0)",
                    parameters = ["Customization_Data/RBC_configuration_layer/Ertms_version/Compatibility_version",
                                  "Customization_Data/RBC_configuration_layer/Ertms_version/Compatibility_within_version"])
# ---------------------------------------------------------------------------------------------------------------------------------------------
sheet.Action("SLR: Inspect SoM Position Report Message 157")
sheet.ExpectedResult("<NID_LRBG> = <Referential/Route/LRBG>")
sheet.ExpectedResult("<Q_STATUS> = 1 (Valid)")
# ---------------------------------------------------------------------------------------------------------------------------------------------
sheet.Action("SLR: Inspect Train Accepted Message 41")
sheet.ExpectedResult("Message is sent")
# ---------------------------------------------------------------------------------------------------------------------------------------------
sheet.Action("SLR: Inspect Validated Train Data Message 129")
sheet.ExpectedResult("Validated Train Data Message 129 is received")
# ---------------------------------------------------------------------------------------------------------------------------------------------
sheet.Action("SLR: Inspect Ack of Train Data Message 8")
sheet.ExpectedResult("<M_ACK> = 1 (Ack required)")
# ---------------------------------------------------------------------------------------------------------------------------------------------
sheet.Action("SLR: Acknowledgement Message 146 is received")
sheet.ExpectedResult("<M_ACK> = 1 (Ack required)",
                     requirements = ["[L161_ETCS2-TRK_sSyRS_00083]"]) # Note: EONBE will always ack data immediately, we can't delay this, to have a message repetition.
# ---------------------------------------------------------------------------------------------------------------------------------------------
sheet.Action("SLR: Inspect MA Request Parameters Packet 57")
sheet.ExpectedResult("<T_MAR> = 255 (Irrelevant)",
                    requirements = ["[L161_ETCS2-TRK_sSyRS_00307]"],
                    parameters = ["Customization_Data/RBC_configuration_layer/ERTMS_system_parameters/t_mar"])

sheet.ExpectedResult("<T_TIMEOUTRQST> = 1023 (Irrelevant)",
                     requirements = ["[L161_ETCS2-TRK_sSyRS_00308]"],
                    parameters = ["Customization_Data/RBC_configuration_layer/ERTMS_system_parameters/t_timeouttrqst"])

sheet.ExpectedResult("<T_CYCRQST> = 5 (seconds)",
                    requirements = ["[L161_ETCS2-TRK_sSyRS_00306]"],
                    parameters = ["Customization_Data/RBC_configuration_layer/ERTMS_system_parameters/t_cycrqst"])
# ---------------------------------------------------------------------------------------------------------------------------------------------
sheet.Action("SLR: Inspect MA Request Message 132")
sheet.ExpectedResult("Message is received")
# ---------------------------------------------------------------------------------------------------------------------------------------------
sheet.Action("SLR: Inspect Track Ahead Free Request Message 34")
sheet.ExpectedResult("TAF Request is NOT received",
                     requirements = ["[L161_ETCS2-TRK_sSyRS_00145]"])
# ---------------------------------------------------------------------------------------------------------------------------------------------
sheet.Action("SLR: Inspect SR Authorisation Message 2")
sheet.ExpectedResult("Message is sent",
                     requirements = ["[L161_ETCS2-TRK_sSyRS_00101]",
                                     "[L161_ETCS2-TRK_sSyRS_00102]",
                                     "[L161_ETCS2-TRK_sSyRS_00103]"])
# ---------------------------------------------------------------------------------------------------------------------------------------------
sheet.Action("SLR: Inspect Position Report Parameters Packet 58")
sheet.ExpectedResult("Packet is sent",
                    requirements = ["[L161_ETCS2-TRK_sSyRS_00439]",
                                    "[L161_ETCS2-TRK_sSyRS_00435]"])

sheet.ExpectedResult("<T_CYCLOC> = 6 (seconds)",
                    parameters = ["Customization_Data/RBC_configuration_layer/ERTMS_system_parameters/t_cycloc"])

sheet.ExpectedResult("<D_CYCLOC> = 327670 (Irrelevant)",
                    parameters = ["Customization_Data/RBC_configuration_layer/ERTMS_system_parameters/d_cycloc"])

sheet.ExpectedResult("<M_LOC> = 1 (Every LRBG)",
                    parameters = ["Customization_Data/RBC_configuration_layer/ERTMS_system_parameters/m_loc"])
# ---------------------------------------------------------------------------------------------------------------------------------------------
sheet.Action("SLR: Inspect National Values Packet 3")

sheet.ExpectedResult("Packet is sent",
                    requirements = ["[L161_ETCS2-TRK_sSyRS_00426]",
                                    "[L161_ETCS2-TRK_sSyRS_00438]",
                                    "[L161_ETCS2-TRK_sSyRS_00441]",
                                    "[L161_ETCS2-TRK_sSyRS_00431]"])

sheet.ExpectedResult("<Q_SCALE> = 1 (1 meter)")

sheet.ExpectedResult("<D_VALIDNV> = 32767 (Now)",
                     requirements = ["[L161_ETCS2-TRK_sSyRS_00432]"])

sheet.ExpectedResult("<NID_C> = 255 and 253",
                    requirements = ["[L161_ETCS2-TRK_sSyRS_00428]"],
                    parameters = [  "Customization_Data/RBC_configuration_layer/national_values/national_values_X1/Nmax_national_area",
                                    "Customization_Data/RBC_configuration_layer/national_values/national_values_X1/AG_nid_c"])

sheet.ExpectedResult("<V_NVSHUNT> = 6 (30 km/h)", 
                    parameters = [  "Customization_Data/RBC_configuration_layer/national_values/national_values_X1/AG_v_nvshunt"])
                    
sheet.ExpectedResult("<V_NVSTFF> = 6 (30 km/h)", 
                    parameters = [  "Customization_Data/RBC_configuration_layer/national_values/national_values_X1/AG_v_nvstff"])

sheet.ExpectedResult("<V_NVONSIGHT> = 6 (30 km/h)", 
                    parameters = [  "Customization_Data/RBC_configuration_layer/national_values/national_values_X1/AG_v_nvonsight"])

sheet.ExpectedResult("<V_NVUNFIT> = 10 (50 km/h)", 
                    parameters = [  "Customization_Data/RBC_configuration_layer/national_values/national_values_X1/AG_v_nvunfit"])

sheet.ExpectedResult("<V_NVREL> = 4 (20 km/h)",
                    parameters = [  "Customization_Data/RBC_configuration_layer/national_values/national_values_X1/AG_v_nvrel"])

sheet.ExpectedResult("<D_NVROLL> = 10 (meters)",
                    parameters = [  "Customization_Data/RBC_configuration_layer/national_values/national_values_X1/AG_d_nvroll"])

sheet.ExpectedResult("<Q_NVSBTSMPERM> = 0 (No Permission to use service brake in target speed monitoring)",
                    parameters = [  "Customization_Data/RBC_configuration_layer/national_values/national_values_X1/AG_q_nvsrbktrg"])

sheet.ExpectedResult("<Q_NVEMRRLS> = 1 (Revoke emergency brake command when permitted speed supervision limit is no longer exceeded)",
                    parameters = [  "Customization_Data/RBC_configuration_layer/national_values/national_values_X1/AG_q_nvemrrls"])

sheet.ExpectedResult("<Q_NVGUIPERM> = 0",
                    requirements = ["[L161_ETCS2-TRK_sSyRS_00430]"],
                    parameters = [  "Customization_Data/RBC_configuration_layer/national_values/national_values_X2/AG_q_nvguiperm"])

sheet.ExpectedResult("<V_NVALLOWOVTRP> = 3 (15 km/h)",
                    parameters = [  "Customization_Data/RBC_configuration_layer/national_values/national_values_X1/AG_v_nvallowovtrp"])

sheet.ExpectedResult("<V_NVSUPOVTRP> = 6 (30 km/h)",
                    parameters = [  "Customization_Data/RBC_configuration_layer/national_values/national_values_X1/AG_v_nvsupovtrp"])

sheet.ExpectedResult("<D_NVOVTRP> = 100 (meters)",
                    parameters = [  "Customization_Data/RBC_configuration_layer/national_values/national_values_X1/AG_d_nvovtrp"])

sheet.ExpectedResult("<T_NVOVTRP> = 255 (seconds)",
                    parameters = [  "Customization_Data/RBC_configuration_layer/national_values/national_values_X1/AG_t_nvovtrp"])

sheet.ExpectedResult("<D_NVPOTRP> = 200 (meters)",
                    parameters = [  "Customization_Data/RBC_configuration_layer/national_values/national_values_X1/AG_d_nvpotrp"])

sheet.ExpectedResult("<M_NVCONTACT> = 1 (Service Brake)",
                    parameters = [  "Customization_Data/RBC_configuration_layer/national_values/national_values_X1/AG_m_nvcontact"])

sheet.ExpectedResult("<T_NVCONTACT> = 40 (seconds)",
                    parameters = [  "Customization_Data/RBC_configuration_layer/national_values/national_values_X1/AG_t_nvcontact"])

sheet.ExpectedResult("<M_NVDERUN> = 0 (Entry of Driver ID not permitted while running)",
                    parameters = [  "Customization_Data/RBC_configuration_layer/national_values/national_values_X1/AG_m_nvderun"])

sheet.ExpectedResult("<D_NVSTFF> = 32767 (Infinite)",
                    parameters = [  "Customization_Data/RBC_configuration_layer/national_values/national_values_X1/AG_d_nvstff"])

sheet.ExpectedResult("<Q_NVDRIVER_ADHES> = 0 (Track adhesion change not allowed)",
                    parameters = [  "Customization_Data/RBC_configuration_layer/national_values/national_values_X1/AG_q_nvdriver_adhes"])
# ---------------------------------------------------------------------------------------------------------------------------------------------
sheet.Action("SLR: Inspect Movement Authority Message 3")
sheet.ExpectedResult("Movement Authority is NOT sent",
                     requirements = ["[L161_ETCS2-TRK_sSyRS_00122]",
                                     "[L161_ETCS2-TRK_sSyRS_00124]",
                                     "[L161_ETCS2-TRK_sSyRS_00131]",
                                     "[L161_ETCS2-TRK_sSyRS_00132]"])

# ---------------------------------------------------------------------------------------------------------------------------------------------
sheet.Action("Drive the train over the SBG closed signal (RNP)\nNote: SBG will send 'Stop if SR' packet")
sheet.ExpectedResult("Position Report Message 136 is received with <M_MODE> = 7 (Trip)",
                     requirements = ["[L161_ETCS2-TRK_sSyRS_00131]",
                                     "[L161_ETCS2-TRK_sSyRS_00132]"])

# *********************************************************************************************************************************************
sheet.Case("SoM in L2 with an INVALID position")
# ---------------------------------------------------------------------------------------------------------------------------------------------
sheet.Action(f"Set a train upstream of signal {signalWithRnp}, reporting on SBG and perform SoM in L2 with a INVALID position")
sheet.ExpectedResult("Session is being established between EONBE and RBC")

# ---------------------------------------------------------------------------------------------------------------------------------------------
sheet.Action("SLR: Inspect SoM Position Report Message 157")
sheet.ExpectedResult("<NID_LRBG> = <Referential/Route/LRBG>")
sheet.ExpectedResult("<Q_STATUS> = 0 (Invalid)")
# ---------------------------------------------------------------------------------------------------------------------------------------------
sheet.Action("SLR: Inspect Train Accepted Message 41")
sheet.ExpectedResult("Message is sent",
                     requirements = ["[L161_ETCS2-TRK_sSyRS_00109]",
                                     "[L161_ETCS2-TRK_sSyRS_00110]"])
# ---------------------------------------------------------------------------------------------------------------------------------------------
sheet.Action("SLR: Inspect SR Authorisation Message 2")
sheet.ExpectedResult("Message is sent",
                     requirements = ["[L161_ETCS2-TRK_sSyRS_00074]",
                                     "[L161_ETCS2-TRK_sSyRS_00077]"],
                     parameters = ["Customization_Data/RBC_configuration_layer/ERTMS_system_parameters/train_always_accepted_on_invalid_position"])
# ---------------------------------------------------------------------------------------------------------------------------------------------
sheet.Action("SLR: Inspect Position Report Message 136")
sheet.ExpectedResult("<M_MODE> = 2 (Staff Responsible)")


# *********************************************************************************************************************************************
sheet.Case("SoM in L2 with an UNKNOWN position")
# ---------------------------------------------------------------------------------------------------------------------------------------------
sheet.Action(f"Set a train upstream of signal {signalWithRnp} and perform SoM in L2 with a UNKNOWN position")
sheet.ExpectedResult("Session is being established between EONBE and RBC")
# ---------------------------------------------------------------------------------------------------------------------------------------------
sheet.Action("SLR: Inspect SoM Position Report Message 157")
sheet.ExpectedResult("<NID_LRBG> = 32767 (Unknown)")
sheet.ExpectedResult("<Q_STATUS> = 2 (Unknown)")
# ---------------------------------------------------------------------------------------------------------------------------------------------
sheet.Action("SLR: Inspect Train Accepted Message 41")
sheet.ExpectedResult("Message is sent",
                     requirements = ["[L161_ETCS2-TRK_sSyRS_00109]",
                                     "[L161_ETCS2-TRK_sSyRS_00110]"])
# ---------------------------------------------------------------------------------------------------------------------------------------------
sheet.Action("SLR: Inspect SR Authorisation Message 2")
sheet.ExpectedResult("Message is sent",
                     requirements = ["[L161_ETCS2-TRK_sSyRS_00075]",
                                     "[L161_ETCS2-TRK_sSyRS_00111]",
                                     "[L161_ETCS2-TRK_sSyRS_00113]"],
                     parameters = ["Customization_Data/RBC_configuration_layer/ERTMS_system_parameters/train_acceptance_on_unknown_position"])
sheet.ExpectedResult("SLR: SR Authorisation <D_SR> = 32767 (Infinite)",
                     requirements = ["[L161_ETCS2-TRK_sSyRS_00671]"])
# ---------------------------------------------------------------------------------------------------------------------------------------------
sheet.Action("SLR: Inspect Position Report Message 136")
sheet.ExpectedResult("<M_MODE> = 2 (Staff Responsible)")
# ---------------------------------------------------------------------------------------------------------------------------------------------
sheet.Action("Wait until a new MA request is received from OBU (5s)")
sheet.ExpectedResult("MA Request Parameters Packet 57 is received")
sheet.ExpectedResult("SLR: Inspect SR Authorisation Message 2")
sheet.ExpectedResult("Message is sent",
                     requirements = ["[L161_ETCS2-TRK_sSyRS_00112]"])


# *********************************************************************************************************************************************
sheet.Case("SoM in L2 with an Valid position but with LRBG not in RBC database")
# ---------------------------------------------------------------------------------------------------------------------------------------------
sheet.Action(f"Set a train upstream of signal {signalWithRnp} and perform SoM in L2 with a VALID position but reporting on a NID_LRBG not part of RBC database")
sheet.ExpectedResult("Session is being established between EONBE and RBC")
# ---------------------------------------------------------------------------------------------------------------------------------------------
sheet.Action("SLR: Inspect SoM Position Report Message 157")
sheet.ExpectedResult("<NID_LRBG> = 99999")
sheet.ExpectedResult("<Q_STATUS> = 1 (Valid)")

# ---------------------------------------------------------------------------------------------------------------------------------------------
sheet.Action("SLR: Inspect SR Authorisation Message 2")
sheet.ExpectedResult("SLR: Message is sent",
                     requirements = ["[L161_ETCS2-TRK_sSyRS_00075]"],
                     parameters = ["Customization_Data/RBC_configuration_layer/ERTMS_system_parameters/train_acceptance_on_unknown_position"])

# *********************************************************************************************************************************************
sheet.Case("Shunting Request in L2 with VALID position")
# ---------------------------------------------------------------------------------------------------------------------------------------------
sheet.Action(f"Set a train upstream of signal {signalWithRnp}, reporting on SBG, with VALID position and request Shunting in Level 2")
# ---------------------------------------------------------------------------------------------------------------------------------------------
sheet.ExpectedResult("SoM Position Report Message 157 is received with <Q_STATUS> = 1")
sheet.ExpectedResult("Request for Shunting Message 130 is received",
                     requirements = ["[L161_ETCS2-TRK_sSyRS_00106]"])
sheet.ExpectedResult("SLR: SH Authorised Message 28 is sent",
                     requirements = ["[L161_ETCS2-TRK_sSyRS_00105]",
                                     "[L161_ETCS2-TRK_sSyRS_00107]",
                                     "[L161_ETCS2-TRK_sSyRS_00108]",])
sheet.ExpectedResult("SLR: National Values Packet 3 is sent.\nNote: Values are checked in SOM test",
                     requirements = ["[L161_ETCS2-TRK_sSyRS_00433]",
                                        "[L161_ETCS2-TRK_sSyRS_00434]"])
sheet.ExpectedResult("<M_MODE> = 3 (Shunting)")

# *********************************************************************************************************************************************
sheet.Case("Shunting Request in L2 with UNKNOWN position")
# ---------------------------------------------------------------------------------------------------------------------------------------------
sheet.Action(f"Set a train upstream of signal {signalWithRnp}, reporting an UNKNOWN position and request Shunting in Level 2")
sheet.ExpectedResult("SLR: SoM Position Report Message 157 is received with <Q_STATUS> = 2 (Unknown)")
sheet.ExpectedResult("SLR: Request for Shunting Message 130 is received")
sheet.ExpectedResult("SLR: SH Authorised Message 28 is sent",
                     requirements = ["[L161_ETCS2-TRK_sSyRS_00115]"])
sheet.ExpectedResult("SLR: National Values Packet 3 is NOT sent (as LRBG is unknown)",
                     requirements = ["[L161_ETCS2-TRK_sSyRS_00434]"])
sheet.ExpectedResult("SLR: SoM Position Report Message 157 <M_MODE> = 3 (Shunting)")


# *********************************************************************************************************************************************
sheet.Case("SoM in L2 with an UNKNOWN position and crossing SBG of signal at RP aspect")
# ---------------------------------------------------------------------------------------------------------------------------------------------
sheet.Action(f"Set a train upstream of signal's {signalWithRp} SBG, occupy track downstream (leading to aspect RP) and perform SoM in L2 with a UNKNOWN position")
sheet.ExpectedResult("SLR: SoM Position Report Message 157 is received with <Q_STATUS> = 2 (Unknown)")
sheet.Action(f"Move the train to cross the SBG and stop before signal {signalWithRp}")
sheet.ExpectedResult("SLR: Position Report Message 136 is received with <LRBG> != 32767 (Not unknown)")
sheet.ExpectedResult("SLR: Mode profile Packet 80 is sent")
sheet.ExpectedResult("SLR: Mode profile <N_ITER> = 1 (Two OS mode profile segments)\nNote: Other OS profiles data are checked in RT_* tests")
sheet.ExpectedResult("SLR: Mode profile <M_MAMODE> for both iterations = 0 (Onsight)",
                        requirements = ["[L161_ETCS2-TRK_sSyRS_00116]",
                                        "[L161_ETCS2-TRK_sSyRS_00117]",
                                        "[L161_ETCS2-TRK_sSyRS_00125]",
                                        "[L161_ETCS2-TRK_sSyRS_00126]"])

# *********************************************************************************************************************************************
sheet.Case("SoM in L2 with an UNKNOWN position and crossing SBG of signal at PROCEED aspect")
# ---------------------------------------------------------------------------------------------------------------------------------------------
sheet.Action(f"Set a train upstream of signal's {signalWithRp} SBG, with track downstream released, and perform SoM in L2 with a UNKNOWN position")
sheet.ExpectedResult("SLR: SoM Position Report Message 157 is received with <Q_STATUS> = 2 (Unknown)")
sheet.Action(f"Move the train to cross the SBG and stop before signal {signalWithRp}")
sheet.ExpectedResult("SLR: Position Report Message 136 is received with <LRBG> != 32767 (Not unknown)")
# ---------------------------------------------------------------------------------------------------------------------------------------------
sheet.ExpectedResult("SLR: National Values Packet 3 is sent.\nNote: Values are checked in SOM test",
                        requirements = ["[L161_ETCS2-TRK_sSyRS_00438]",
                                        "[L161_ETCS2-TRK_sSyRS_00440]"])
sheet.ExpectedResult("SLR: Movement Authority Message 3 is sent",
                        requirements = ["[L161_ETCS2-TRK_sSyRS_00240]"])
sheet.ExpectedResult("SLR: Mode profile Packet 80 is sent")
sheet.ExpectedResult("SLR: Mode profile <N_ITER> = 0 (One OS mode profile segment only)\nNote: Other OS profiles data are checked in RT_* tests")
sheet.ExpectedResult("SLR: Mode profile <M_MAMODE> = 0 (Onsight)", 
                        requirements = ["[L161_ETCS2-TRK_sSyRS_00118]",
                                        "[L161_ETCS2-TRK_sSyRS_00119]",
                                        "[L161_ETCS2-TRK_sSyRS_00127]",
                                        "[L161_ETCS2-TRK_sSyRS_00128]"])

# *********************************************************************************************************************************************
sheet.Case("SoM in L2 with an UNKNOWN position and crossing SBG of signal at R+W aspect")
# ---------------------------------------------------------------------------------------------------------------------------------------------
sheet.Action(f"Set a train upstream of signal's {signalWithRp} SBG, with track downstream released, and perform SoM in L2 with a UNKNOWN position")
sheet.ExpectedResult("SLR: SoM Position Report Message 157 is received with <Q_STATUS> = 2 (Unknown)")
sheet.Action(f"Move the train to cross the SBG and stop before signal {signalWithRp}")
sheet.ExpectedResult("SLR: Position Report Message 136 is received with <LRBG> != 32767 (Not unknown)")
sheet.ExpectedResult("SLR: Mode profile Packet 80 is sent")
sheet.ExpectedResult("SLR: Mode profile <N_ITER> = 0 (One OS mode profile segment only)\nNote: Other OS profiles data are checked in RT_* tests")
sheet.ExpectedResult("SLR: Mode profile <M_MAMODE> = 0 (Onsight)", 
                        requirements = ["[L161_ETCS2-TRK_sSyRS_00121]",
                                        "[L161_ETCS2-TRK_sSyRS_00130]"])
sheet.ExpectedResult("SLR: Mode profile <M_MAMODE> = 1 (Shunting)", 
                        requirements = ["[L161_ETCS2-TRK_sSyRS_00120]",
                                        "[L161_ETCS2-TRK_sSyRS_00121]",
                                        "[L161_ETCS2-TRK_sSyRS_00129]",
                                        "[L161_ETCS2-TRK_sSyRS_00130]"])

# *********************************************************************************************************************************************
sheet.Case("SoM in L2 with an UNKNOWN position and crossing IBG of signal at PROCEED aspect")
# ---------------------------------------------------------------------------------------------------------------------------------------------
sheet.Action(f"Set a train upstream of signal's {signalWithRp} IBG (=beyond TAF limits), with track downstream released, and perform SoM in L2 with a UNKNOWN position")
sheet.ExpectedResult("SLR: SoM Position Report Message 157 is received with <Q_STATUS> = 2 (Unknown)")
sheet.Action(f"Move the train to cross the IBG")
sheet.ExpectedResult("SLR: Movement Authority is NOT sent",
                     requirements = ["[L161_ETCS2-TRK_sSyRS_00135]"])

sheet.Save()