"""
Retrieve, format and return recent data.
"""
import json
from apis.ebird import requester
from apis.ebird import reformat

def region_checklists(region):
    """ Latest 10 checklists submitted for the subregion """
    region_code = reformat.extract_region_code(region)
    response = json.loads(requester.region_checklists(region_code))
    return reformat.extract_hotspots(response)

def region_notable(region, days):
    """ Notables """
    region_code = reformat.extract_region_code(region)
    response = json.loads(requester.region_notable(region_code, days))
    return response

def region_species_obs(region, full_name, days):
    """ Species """
    region_code = reformat.extract_region_code(region)
    species_code = reformat.extract_text_between_brackets(full_name)
    response = json.loads(requester.region_species_obs(region_code, species_code, days))
    return response

def region_location_obs(location_id, days):
    """ Location species """
    response = json.loads(requester.region_location_obs(location_id, days))
    return response

def region_hotspots(region):
    """ Hotspots """
    region_code = reformat.extract_region_code(region)
    response = json.loads(requester.region_hotspots(region_code))
    return response
