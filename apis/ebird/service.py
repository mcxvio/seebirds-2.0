"""
Retrieve, format and return recent data.
"""
import json
import ijson

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

def region_species_code_obs(region, species_code, days):
    """ Species """
    region_code = reformat.extract_region_code(region)
    response = json.loads(requester.region_species_obs(region_code, species_code, days))
    return response

def region_species_obs(region, full_name, days):
    """ Species """
    region_code = reformat.extract_region_code(region)
    species_code = reformat.extract_text_between_brackets(full_name)
    response = json.loads(requester.region_species_obs(region_code, species_code, days))
    return response

def region_species_historic_obs(region_code, historic_date):
    response = json.loads(requester.region_species_historic_obs(region_code, historic_date.replace("-", "/")))
    return response

def region_location_obs(location_id, days):
    """ Location species """
    response = json.loads(json.loads(requester.region_location_obs(location_id, days)))
    return response

def region_hotspots(region):
    """ Hotspots """
    region_code = reformat.extract_region_code(region)
    response = json.loads(requester.region_hotspots(region_code))
    return response

def region_hotspots_all(region):
    """ Hotspots """
    region_code = reformat.extract_region_code(region)
    return requester.region_hotspots(region_code)

def family_species(family):
    """ Family species """
    response = ""
    with open('data_taxaspecies.json') as json_data_file:
        data = ijson.items(json_data_file, 'response.taxa.item')
        species = (s for s in data if s.get("familyComName") is not None
                   and s["familyComName"] == family)

        response = list(species)
    return response

def order_species(order):
    """ Order species """
    response = ""
    with open('data_taxaspecies.json') as json_data_file:
        data = ijson.items(json_data_file, 'response.taxa.item')
        species = (s for s in data if s.get("order") is not None
                   and s["order"] == order)

        response = list(species)
    return response

def extinct_species_all():
    """ Extinct species. """
    response = ""
    with open('data_taxaspecies.json') as json_data_file:
        data = ijson.items(json_data_file, 'response.taxa.item')
        species = (s for s in data if s.get("extinct") is not None and s["extinct"])

        response = list(species)
    return response
