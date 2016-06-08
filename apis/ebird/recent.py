import json
from apis.ebird import raw
from apis.ebird import reformat

# checklists
def region_obs(region):
    subregion = reformat.extractRegionCode(region)
    rtype = reformat.extractRegionType(subregion)
    response = json.loads(raw._region_obs(rtype, subregion))
    # Wrangle the json for html template.
    uniqueDates = reformat.extractUniqueDates(response)

    submissions = []
    submission = {}
    checklists = []
    prevDate = ""
    currDate = ""
    chkCount = 0
    for item in uniqueDates:
        currDate = reformat.extractDateTime(item, 'd')
        if prevDate == "":
            prevDate = currDate
        if prevDate != currDate:
            # Add each date's checklist to the checklists deck.
            reformat.addChecklistsForDate(prevDate, checklists, submission, submissions)
            submission = {}
            checklists = []
            prevDate = currDate

        obs = [x for x in response if x['obsDt'] == item] #get checklist's sightings for each date.
        ob = obs[0] #save the first sighting to be used as output.
        reformat.removeObItems(ob)
        ob['obsTm'] = reformat.extractDateTime(item, 't')
        ob['speciesCount'] = len(obs) #total number of species seen.
        checklists.append(ob)
        chkCount = (chkCount + 1)

    # Add last date's checklist to the checklists deck.
    reformat.addChecklistsForDate(currDate, checklists, submission, submissions)
    submissions.append({'chkCount': chkCount}) #number of checklists for a date.
    submission = {}
    checklists = []

    return submissions

# notables
def region_notable(region):
    subregion = reformat.extractRegionCode(region)
    rtype = reformat.extractRegionType(subregion)
    response = json.loads(raw._region_notable(rtype, subregion))
    # Wrangle the json for html template.
    # ...
    return response

# location; empty if location is not valid.
def hotspot_obs(locationId):
    response = json.loads(raw._hotspot_obs(locationId))
    # Wrangle the json for html template.
    # ...
    return response

# species
def region_species_obs(region, fullName):
    subregion = reformat.extractRegionCode(region)
    rtype = reformat.extractRegionType(subregion)
    sciName = reformat.extractScientificName(fullName)
    # Wrangle the json for html template.
    # ...
    response = json.loads(raw._region_species_obs(rtype, subregion, sciName))
    return response
