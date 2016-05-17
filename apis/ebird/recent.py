import requests

#checklists
def region_obs(rtype, subregion):
    response = requests.get("http://ebird.org/ws1.1/data/obs/region/recent?rtype=" + rtype + "&r=" + subregion + "&hotspot=true&includeProvisional=true&back=5&fmt=json")

    if (response.status_code == 400):
        # Bad gateway for invalid data, extract error message.
        assert response.status_code == 400
    else:
        assert response.status_code == 200

    return response.text

#notables
def region_notable(rtype, subregion):
    response = requests.get("http://ebird.org/ws1.1/data/notable/region/recent?rtype=" + rtype + "&r=" + subregion + "&detail=full&hotspot=true&back=5&fmt=json")

    if (response.status_code == 400):
        # Bad gateway for invalid data, extract error message.
        assert response.status_code == 400
    else:
        assert response.status_code == 200

    return response.text

#location; empty if location is not valid.
def hotspot_obs(locationId):
    response = requests.get("http://ebird.org/ws1.1/data/obs/hotspot/recent?r=" + locationId + "&detail=full&includeProvisional=true&back=10&fmt=json")

    assert response.status_code == 200

    return response.text

#species
def region_species_obs(rtype, subregion, sciName):
    response = requests.get("http://ebird.org/ws1.1/data/obs/region_spp/recent?rtype=" + rtype + "&r=" + subregion + "&sci=" + sciName + "&hotspot=true&includeProvisional=true&back=10&fmt=json")

    if (response.status_code == 400):
        # Bad gateway for invalid data, extract error message.
        assert response.status_code == 400
    else:
        assert response.status_code == 200

    return response.text
