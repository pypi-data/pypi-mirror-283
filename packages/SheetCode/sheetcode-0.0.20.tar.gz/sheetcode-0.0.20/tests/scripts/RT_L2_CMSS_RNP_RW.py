from SheetCode import Sheet
import scripts.RT_Common as RT_Common

sheet = Sheet(__file__)

sheet.Name = "Elementary routes inside Level 2 area from Controlled Main Stop Signals switching from RNP to RED+WHITE aspect"
sheet.Description = ["For each route marked with Referential/Route/@Type='Inside' and with <Referential/Route/PossibleModes> = SH:",
                      "1) A train is placed upstream the closed start signal showing RNP aspect and we perform a SoM with Valid position. We check:",
                      "- MA up to start signal. (Note: Other aspects of this MA are checked is the same test for the previous route upstream)",
                      "- Mode profile OS up to start signal"
                      "2) Route is set in SH mode, signal switches to RED+WHITE aspect. We will check:",
                      "- MA (Length, Release Speed, Danger point, absence of section timers & overlap)",
                      "- Gradient profile",
                      "- Linking",
                      "- SSP for each category",
                      "- Mode profile OS up to start signal",
                      "- Mode profile SH from start to end signal",
                      "3) Train is driven past the start signal. We check transition to SH mode"]

sheet.StartConditions = ["No elementary routes is set or locked.",
                        "No train is set on the track."]

# *********************************************************************************************************************************************
sheet.Case(f"Route set in SH")
RT_Common.InitialConditionsL2(sheet, RT_Common.Aspects.RNP, RT_Common.InitialPositions.Valid)
# ---------------------------------------------------------------------------------------------------------------------------------------------
sheet.Action(f"Set route under test in SH")
RT_Common.ExpectedResultsRouteCommons(sheet, RT_Common.Aspects.RW)
# ---------------------------------------------------------------------------------------------------------------------------------------------
sheet.Action("Drive past the signal")
RT_Common.ExpectedResultsDrivePastSignal(sheet, RT_Common.Aspects.RW)

sheet.Save()
