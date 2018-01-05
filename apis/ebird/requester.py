"""
Query eBird 2.0 API.
"""
import json
import requests

def get_ebird_key():
    """ Get the eBird key for API 2.0 """
    with open('keys.json') as json_data_file:
        data = json.load(json_data_file)
    return data['ebird_key']

def region_checklists(region_code):
    """ recent checklists """
    response = requests.get("https://ebird.org/ws2.0/product/lists/"
                            + region_code
                            + "?maxResults=20",
                            headers=get_ebird_key())

    if response.status_code == 400:
        # Bad gateway for invalid data, extract error message.
        assert response.status_code == 400
    elif response.status_code == 503:
        # Forbidden, likely bad ebird key.
        assert response.status_code == 503
    else:
        assert response.status_code == 200

    return response.text

def region_obs(subregion):
    """ checklists """
    response = requests.get("https://ebird.org/ws2.0/data/obs/"
                            + subregion
                            + "/recent"
                            + "?hotspot=true&includeProvisional=true&back=1",
                            headers=get_ebird_key())

    if response.status_code == 400:
        # Bad gateway for invalid data, extract error message.
        assert response.status_code == 400
    elif response.status.code == 503:
        # Forbidden, likely bad ebird key.
        assert response.status_code == 503
    else:
        assert response.status_code == 200

    return response.text
