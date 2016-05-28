import json
from apis.ebird import raw
from apis.ebird import reformat

# checklists
def region_obs(region):
    subregion = reformat.extractRegionCode(region)
    rtype = reformat.extractRegionType(subregion)
    response = json.loads(raw._region_obs(rtype, subregion))
    # Wrangle the json for html template.
    uniqueDates = []
    for item in response:
        if not item['obsDt'] in uniqueDates:
            uniqueDates.append(item['obsDt'])

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
            submission['obsDt'] = prevDate
            submission['checklists'] = checklists
            submissions.append(submission)
            submission = {}
            checklists = []
            prevDate = currDate

        obs = [x for x in response if x['obsDt'] == item]
        ob = obs[0]
        del ob['sciName']
        del ob['comName']
        del ob['howMany']
        del ob['obsValid']
        del ob['obsReviewed']
        ob['obsTm'] = reformat.extractDateTime(item, 't')
        ob['speciesCount'] = len(obs)
        checklists.append(ob)
        chkCount = (chkCount + 1)

    # Add last date's checklist to the checklists deck.
    submission['obsDt'] = currDate
    submission['checklists'] = checklists
    submissions.append(submission)
    submissions.append({'chkCount': chkCount})
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
