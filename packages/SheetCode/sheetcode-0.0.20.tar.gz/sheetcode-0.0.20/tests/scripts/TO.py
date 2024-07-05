from SheetCode import Sheet
import scripts.RT_Common as RT_Common

sheet = Sheet(__file__)

sheet.Name = "Track Occupation"
sheet.Description =["For each Referential/TrackOccupations/TrackOccupation, check the state of RBC Track Occupation object when track is occupied and released."]

sheet.StartConditions = ["All track circuits are released"]

# *********************************************************************************************************************************************
sheet.Case("Track occupations")

# ---------------------------------------------------------------------------------------------------------------------------------------------
sheet.Action("Occupy the track circuit")
sheet.ExpectedResult("SLR: <Object_DYN_TRACK_OCCUPATION/track_occupation/occupation_status> = OCCUPIED",
                     parameters = ["Route_Map/RM_interlocking_layer/track_occupations/track_occupation/occupation_status",
                                   "LK/Output/Track occupations/occupation_status_is_clear"])

# ---------------------------------------------------------------------------------------------------------------------------------------------
sheet.Action("Release the track circuit")
sheet.ExpectedResult("SLR: <Object_DYN_TRACK_OCCUPATION/track_occupation/occupation_status> = RELEASED",
                     parameters = ["Route_Map/RM_interlocking_layer/track_occupations/track_occupation/occupation_status",
                                   "LK/Output/Track occupations/occupation_status_is_clear"])

sheet.Save()









