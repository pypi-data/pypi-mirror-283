
from SheetCode import Sheet

sheet = Sheet(__file__)

sheet.Name = "Test Loop Example"
sheet.Description = ["Test loop example"]

sheet.StartConditions = [""]

routes = ["A44_A45", "A45_A46", "A46_A47", "A47_A48", "A48_A49"]

for route in routes:
    sheet.StartLoop(route)

    sheet.Case("Case A")

    sheet.Action("Action 1")

    sheet.ExpectedResult("Expected Result 1",
                            requirements = ["[SIMPLE_REQ_1]"],
                            parameters = ["parameters/yellow_light_enabled"])
    
    sheet.Result(True, "actualValue", "expectedValue")
    
    sheet.ExpectedResult("Expected Result 2",
                            requirements = ["[SIMPLE_REQ_2]"],
                            parameters = ["parameters/yellow_light_enabled"])

    sheet.Result(False)

    sheet.Action("Action 2")

    sheet.ExpectedResult("Expected Result 3",
                            requirements = ["[SIMPLE_REQ_3]"],
                            parameters = ["parameters/yellow_light_enabled"])
    
    sheet.Result(False if route == "A45_A46" else True, "actualValue")

sheet.StopLoop() 

sheet.Save()