from apis.ebird import recent
from apis.ebird import reformat
from flask import Flask
from flask import render_template

app = Flask(__name__)
'''
@app.template_filter('getdatetime')
def datetimeformatter(value, dateortime):
    return reformat.extractDateTime(value, dateortime)
app.jinja_env.filters['getdatetime'] = datetimeformatter
'''
@app.route('/')
@app.route('/index.html')
def index():
    #return 'Welcome to Murmuation :: worldwide birding data!'
    return app.send_static_file('index.html')

@app.route('/outdoors')
def outdoors():
    return app.send_static_file('outdoors.html')

# checklists
@app.route('/checklists/<string:region>', methods=['GET'])
def get_checklists(region):
    data = recent.region_obs(region)
    return render_template('submissions_results.html', data=data, region=region)

# notables
@app.route('/notables/<string:region>', methods=['GET'])
def get_notables(region):
    data = recent.region_notable(region)
    return render_template('sightings_results.html', data=data, region=region)

# location
@app.route('/location/<string:location_id>', methods=['GET'])
def get_location(location_id):
    data = recent.hotspot_obs(location_id)
    return render_template('location_results.html', data=data)

# species
@app.route('/species/<string:region>/<string:fullName>', methods=['GET'])
def get_species(region, fullName):
    data = recent.region_species_obs(region, fullName)
    return render_template('species_results.html', data=data, name=fullName)

if __name__ == '__main__':
    app.run(debug=True)