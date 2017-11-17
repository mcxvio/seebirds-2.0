"""
Main entry to application.
"""
from apis.ebird import recent
from apis.ebird import reformat
from flask import Flask
from flask import render_template

app = Flask(__name__)
app.config.from_pyfile('app.cfg')

@app.template_filter('getdatetime')
def datetimeformatter(value, dateortime):
    """ Date time formatter. """
    return reformat.extract_date_time(value, dateortime)
app.jinja_env.filters['getdatetime'] = datetimeformatter

@app.route('/')
@app.route('/index.html')
def index():
    """ Show index page. """
    #return 'Welcome to Murmuation :: worldwide birding data!'
    return app.send_static_file('index.html')

@app.route('/outdoors')
def outdoors():
    """ Show outdoors page. """
    return app.send_static_file('outdoors.html')

# checklists
@app.route('/checklists/<string:region>', methods=['GET'])
def get_checklists(region):
    """ Show checklists. """
    data = recent.region_obs(region)
    return render_template('submissions_results.html', data=data, region=region)

# notables
@app.route('/notables/<string:region>', methods=['GET'])
def get_notables(region):
    """ Show notable sightings page. """
    data = recent.region_notable(region)
    return render_template('sightings_results.html', data=data, region=region)

# location
@app.route('/location/<string:location_id>', methods=['GET'])
def get_location(location_id):
    """ Show locations page. """
    data = recent.hotspot_obs(location_id)
    return render_template('location_results.html', data=data)

# species
@app.route('/species/<string:region>/<string:fullName>', methods=['GET'])
def get_species(region, full_name):
    """ Show species page. """
    data = recent.region_species_obs(region, full_name)
    return render_template('species_results.html', data=data, name=full_name)

@app.route("/test")
def test():
    """ Show test page. """
    return "<strong>It's Alive!</strong>"


if __name__ == '__main__':
    app.run(app.config['IP'], app.config['PORT'])
    #app.run(debug=True)
