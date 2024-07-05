from SheetCode import Sheet
sheet = Sheet(__file__)

sheet.Name = "Inspection of the referential"
sheet.Description =["Check that the referential is built according to requirements"]

sheet.StartConditions = ["n.a."]

sheet.Case(f"Inspection of referential")
sheet.Action("Inspect referential")
sheet.ExpectedResult("Balise groups (from the BG-A (included) in the entry direction or up to LTO-OUT (included) of the L1S2 in exit direction) are defined in the linking information, except for the TBL1+ BG_IN (the TBL1+BG_IN for the project are 255_08473 and 255_01878 and there is no TBL1+BG_OUT).", 
                    requirements = ["[L161_ETCS2-TRK_sSyRS_00361]"])
sheet.ExpectedResult("Q_LOCACC for non-duplicated balise groups (with M_DUP=0) = 5 meters", 
                    requirements = ["[L161_ETCS2-TRK_sSyRS_00363]"])
sheet.ExpectedResult("Q_LOCACC for duplicated balise groups (with M_DUP <> 0) = 8m", 
                    requirements = ["[L161_ETCS2-TRK_sSyRS_00364]"])
sheet.ExpectedResult("Q_LINKREACTION = 2 (No Reaction) for all BGs except PBGs, SBG of L1 Signal 2's", 
                    requirements = ["[L161_ETCS2-TRK_sSyRS_00365]"])
sheet.ExpectedResult("Q_LINKREACTION = 0 (Train Trip) for PBGs", 
                    requirements = ["[L161_ETCS2-TRK_sSyRS_00365]"])
sheet.ExpectedResult("Q_LINKREACTION = 1 (Service Brake) for SBG on L1 Signal 2's", 
                    requirements = ["[L161_ETCS2-TRK_sSyRS_00365]"])
sheet.ExpectedResult("For Controlled Main Stop Signals, V_RELEASEDP = 6 (30 km/h) if Danger Point distance > 300m", 
                    requirements = ["[L161_ETCS2-TRK_sSyRS_00369]"])
sheet.ExpectedResult("For Controlled Main Stop Signals, V_RELEASEDP = 3 or 4 (resp 15 or 20 km/h) if Danger Point distance <= 300m\n. Note: Actual value is set according to 'Element SI NLS' file from customer's DEI", 
                    requirements = ["[L161_ETCS2-TRK_sSyRS_00370]"])
sheet.ExpectedResult("For Non-Controlled Main Stop Signals, V_RELEASEDP = 6 (30 km/h)", 
                    requirements = ["[L161_ETCS2-TRK_sSyRS_00371]"])
sheet.ExpectedResult("For stopping points associated to REAL buffer stops, V_RELEASEDP = 3 (15 km/h)", 
                    requirements = ["[L161_ETCS2-TRK_sSyRS_00372]"])
sheet.ExpectedResult("Entry routes are starting at signals A52, BX52, TJ8, TXJ8, AX145, B145, AZ252, BY252",
                    requirements = ["[L161_ETCS2-TRK_sSyRS_00539]"])
sheet.ExpectedResult("NID_STM declared in Packet 41 are 28 (TBL1+) and 7 (TBL2)",
                    requirements = ["[L161_ETCS2-TRK_sSyRS_00501]"])
sheet.Save()