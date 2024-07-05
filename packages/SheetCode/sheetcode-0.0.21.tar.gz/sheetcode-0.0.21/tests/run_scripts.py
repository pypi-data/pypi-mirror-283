import sys;sys.path.append(".")
from SheetCode import Scripts, Traceability, Summary

Scripts.Configure(specId = "RM",
                  specVersion = "1A",
                  scriptsPath = "tests/scripts",
                  sheetsPath = "tests/sheets",
                  traceabilityPath = "tests/traceability",
                  summaryPath = "tests/summary",
                  rvtFilepath = "../DAA-000048 RVT/2A - Ongoing/DAA-000048_2A.xlsm",
                  parametersFilepath = "../Traceability/A-0000175109 1B App A_Traceability_RBC_9.4.0.xlsm",
                  mode = Scripts.Mode.Specification)

Traceability.Clear()
Summary.Clear()

#Scripts.Run(["RT_L2_CMSS_RNP_RW"])

Scripts.RunAll()

Traceability.EvaluateSheetsCoverage("RBC Data Validation RM")


