import requests

def get_location_obs():
    response = requests.get('http://ebird.org/ws1.1/data/obs/loc/recent?r=L99381&fmt=json')

    assert response.status_code == 200

    return response.text
