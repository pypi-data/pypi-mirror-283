from SheetCode import Sheet
sheet = Sheet(__file__)

sheet.Name = "Inspection of the RBC Middleware Data Preparation"
sheet.Description =["TBD"]

sheet.StartConditions = ["n.a."]

sheet.Case(f"Inspection of Safe_Kernel_RBC.xml")
sheet.Action("Inspect XML")
sheet.ExpectedResult("ES_SEND_USED_CHANNEL = NP_CHANNEL",
                    requirements = ["[L161_ETCS2-TRK_sSyRS_00201]"])
sheet.ExpectedResult("MOBILE_TIMEOUT_DURATION_EVC = 180",
                    requirements = ["[L161_ETCS2-TRK_sSyRS_00660]",
                                    "[L161_ETCS2-TRK_sSyRS_00661]"])

sheet.Case(f"Inspection of Safe_Netw_RBC.xml")

sheet.Case(f"Inspection of NSafe_Kernel_RBC.xml")

sheet.Case(f"Inspection of NSafe_Netw_RBC.xml")

sheet.Save()