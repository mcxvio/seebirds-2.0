"""
Retrieve, format and return recent data.
"""
import json
from apis.ebird import requester
from apis.ebird import requester_v1_1
from apis.ebird import reformat

### eBird 2.0 ###
def region_checklists(region):
    """ Latest 10 checklists submitted for the subregion """
    subregion = reformat.extract_region_code(region)
    response = json.loads(requester.region_checklists(subregion))
    return reformat.extract_hotspots(response)

### eBird 1.1 ###
def region_obs(region):
    """ checklists """
    subregion = reformat.extract_region_code(region)
    rtype = reformat.extract_region_type(subregion)
    response = json.loads(requester_v1_1.region_obs(rtype, subregion))
    # Wrangle the json for html template ->
    #    {
    #        "obsDt": extract_date_time(item['obsDt'], 'd'),
    #        "checklists": [{"locID": item['locID'],
    #        "locName": item['locName'],
    #        "obsTm": extract_date_time(item['obsDt'], 't'),
    #        "speciesCount": speciesCount}]
    #    }
    unique_date_times = reformat.extract_unique_date_times(response)

    submissions = []
    submission = {}
    checklists = []
    prev_date = ""
    curr_date = ""
    check_count = 0
    for item in unique_date_times:
        curr_date = reformat.extract_date_time(item, 'da')
        if prev_date == "":
            prev_date = curr_date
        if prev_date != curr_date:
            # Add each date's checklist to the checklists deck.
            reformat.add_checklists_for_date(prev_date, checklists, submission, submissions)
            submission = {}
            checklists = []
            prev_date = curr_date

        #get checklist's sightings for each date.
        obs = [x for x in response if x['obsDt'] == item]
        observation = obs[0] #save the first sighting to be used as output.
        reformat.remove_ob_items(observation)
        observation['obsTm'] = reformat.extract_date_time(item, 't')
        observation['speciesCount'] = len(obs) #total number of species seen.
        checklists.append(observation)
        check_count = (check_count + 1)

    # Add last date's checklist to the checklists deck.
    reformat.add_checklists_for_date(curr_date, checklists, submission, submissions)
    submissions.append({'chkCount': check_count}) #number of checklists for a date.
    submission = {}
    checklists = []

    return submissions

def region_notable_wrangle(region):
    """ Region notable wrangle. """
    subregion = reformat.extract_region_code(region)
    rtype = reformat.extract_region_type(subregion)
    response = json.loads(requester_v1_1.region_notable(rtype, subregion))

    # Extracting the dates in the following way makes the template code simpler
    # but loses the time which needs to be displayed.
    # Wrangle the json for html template.
    unique_dates = []
    for item in response:
        if not reformat.extract_date_time(item['obsDt'], 'dx') in unique_dates:
            unique_dates.append(reformat.extract_date_time(item['obsDt'], 'dx'))

    sightings = []
    sighting = {}
    for item in unique_dates:
        print("item ", item)
        #get checklist's sightings for each date.
        obs = [x for x in response if reformat.extract_date_time(x['obsDt'], 'dx') == item]
        sighting['obsDt'] = item
        sighting['species'] = obs
        sightings.append(sighting)
        sighting = {}

    return sightings

def region_notable(region):
    """ Notables """
    subregion = reformat.extract_region_code(region)
    rtype = reformat.extract_region_type(subregion)
    response = json.loads(requester_v1_1.region_notable(rtype, subregion))
    return response

def hotspot_obs(location_id):
    """ location; empty if location is not valid. """
    response = json.loads(requester_v1_1.hotspot_obs(location_id))
    # Wrangle the json for html template.
    # ...
    return response

def region_species_obs(region, full_name):
    """ species """
    subregion = reformat.extract_region_code(region)
    rtype = reformat.extract_region_type(subregion)
    sci_name = reformat.extract_scientific_name(full_name)
    # Wrangle the json for html template.
    # ...
    response = json.loads(requester_v1_1.region_species_obs(rtype, subregion, sci_name))
    return response
