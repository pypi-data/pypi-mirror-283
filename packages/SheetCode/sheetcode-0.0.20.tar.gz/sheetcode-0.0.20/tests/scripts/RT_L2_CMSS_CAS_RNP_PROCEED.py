from SheetCode import Sheet
import scripts.RT_Common as RT_Common

sheet = Sheet(__file__)

sheet.Name = "Elementary routes inside Level 2 area from Controlled Main Stop Signals & Controlled Automatic Signals switching from RNP to PROCEED"
sheet.Description = ["For each route marked with Referential/Route/@Type='Inside' and with <Referential/Route/PossibleModes> = FS",
                      "1) A train is placed upstream of the closed start signal showing RNP aspect and we perform a SoM with Valid position. We check:",
                      "- MA up to start signal. (Note: Other aspects of this MA are checked is the same test for the previous route upstream)",
                      "- Mode profile OS up to start signal"
                      "2) Route is set in FS mode, so signal will switch to PROCEED aspect. We will check:",
                      "- MA (Length, Release Speed, Danger point, absence of section timers & overlap)",
                      "- Gradient profile",
                      "- Linking",
                      "- SSP for each category",
                      "- Mode profile (depending on mode set)",
                      "3) Train is driven past the start signal. We check transition to FS mode"]

sheet.StartConditions = ["No elementary routes is set or locked.",
                          "No train is set on the track."]

# *********************************************************************************************************************************************
sheet.Case(f"Route set in FS")
RT_Common.InitialConditionsL2(sheet, RT_Common.Aspects.RNP, RT_Common.InitialPositions.Valid)
# ---------------------------------------------------------------------------------------------------------------------------------------------
sheet.Action(f"Set route under under test in FS")
RT_Common.ExpectedResultsRouteCommons(sheet, RT_Common.Aspects.PROCEED)
# ---------------------------------------------------------------------------------------------------------------------------------------------
sheet.Action("Drive past the signal")
RT_Common.ExpectedResultsDrivePastSignal(sheet, RT_Common.Aspects.PROCEED)

sheet.Save()
