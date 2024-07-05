from SheetCode import Sheet
import scripts.RT_Common as RT_Common

sheet = Sheet(__file__)

sheet.Name = "Elementary routes inside Level 2 area from Non-Controlled Main Stop Signals switching from RP to PROCEED"
sheet.Description = ["For each route marked with Referential/Route/@Type='Inside' and with <Referential/Route/PossibleModes> = OS:",
                      "1) A train is placed upstream the closed start signal whose downstream section is occupied, hence showing RP aspect and we perform a SoM with Valid position. We check:",
                      "- MA up to start signal. (Note: Other aspects of this MA are checked is the same test for the previous route upstream)",
                      "- Mode profile OS in up to END signal"
                      "2) Track occupation downstream signal is released. Signal shows PROCEED aspect. We check:",
                      "- MA (Length, Release Speed, Danger point, absence of section timers & overlap)",
                      "- Gradient profile",
                      "- Linking",
                      "- SSP for each category",
                      "- Mode profile OS reduced up to the START signal",
                      "3) Train is driven past the start signal. We check transition to FS mode"]

sheet.StartConditions = ["No elementary routes is set or locked.",
                        "No train is set on the track."]

# *********************************************************************************************************************************************
sheet.Case(f"Route set in FS")
RT_Common.InitialConditionsL2(sheet, RT_Common.Aspects.RP, RT_Common.InitialPositions.Valid)
# ---------------------------------------------------------------------------------------------------------------------------------------------
sheet.Action(f"Set route under test in FS")
RT_Common.ExpectedResultsRouteCommons(sheet, RT_Common.Aspects.PROCEED)
# ---------------------------------------------------------------------------------------------------------------------------------------------
sheet.Action("Drive past the signal")
RT_Common.ExpectedResultsDrivePastSignal(sheet, RT_Common.Aspects.PROCEED)

sheet.Save()