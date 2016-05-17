from apis.ebird import recent
from apis.ebird import reformat
from flask import Flask

app = Flask(__name__)

@app.route('/')
@app.route('/index.html')
def index():
    #return 'Welcome to Murmuation :: worldwide birding data!'
    return app.send_static_file('index.html')

@app.route('/outdoors')
def outdoors():
    return app.send_static_file('outdoors.html')

@app.route('/checklists/<string:region>', methods=['GET'])
def get_checklists(region):
    subregion = reformat.extractRegionCode(region)
    rtype = reformat.extractRegionType(subregion)

    response = recent.region_obs(rtype, subregion)

    return response

@app.route('/notables/<string:region>', methods=['GET'])
def get_notables(region):
    subregion = reformat.extractRegionCode(region)
    rtype = reformat.extractRegionType(subregion)

    response = recent.region_notable(rtype, subregion)

    return response

@app.route('/location/<string:location_id>', methods=['GET'])
def get_location(location_id):
    response = recent.hotspot_obs(location_id)

    return response

@app.route('/species/<string:region>/<string:fullName>', methods=['GET'])
def get_species(region, fullName):
    subregion = reformat.extractRegionCode(region)
    rtype = reformat.extractRegionType(subregion)
    sciName = reformat.extractScientificName(fullName)

    response = recent.region_species_obs(rtype, subregion, sciName)

    return response

if __name__ == '__main__':
    app.run(debug=True)