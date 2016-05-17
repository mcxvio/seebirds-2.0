from apis.ebird import recent
from apis.ebird import format
from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return 'Welcome to Murmuation :: worldwide birding data!'

@app.route('/checklists/<string:region>', methods=['GET'])
def get_checklists(region):
    subregion = format.extractRegionCode(region)
    rtype = format.extractRegionType(subregion)

    response = recent.region_obs(rtype, subregion)

    return response

@app.route('/notables/<string:region>', methods=['GET'])
def get_notables(region):
    subregion = format.extractRegionCode(region)
    rtype = format.extractRegionType(subregion)

    response = recent.region_notable(rtype, subregion)

    return response

@app.route('/location/<string:location_id>', methods=['GET'])
def get_location(location_id):
    response = recent.hotspot_obs(location_id)

    return response

@app.route('/species/<string:region>/<string:sciName>', methods=['GET'])
def get_species(region, sciName):
    subregion = format.extractRegionCode(region)
    rtype = format.extractRegionType(subregion)

    response = recent.region_species_obs(rtype, subregion, sciName)

    return response

if __name__ == '__main__':
    app.run(debug=True)