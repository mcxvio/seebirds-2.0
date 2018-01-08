"""
Main entry to application.
"""
from apis.ebird import service
from apis.ebird import reformat
from apis.ebird import history as searches
from flask import Flask
from flask import render_template
from flask import redirect
# session management
from flask_session import Session

app = Flask(__name__)
app.config.from_pyfile('app.cfg')

@app.template_filter('getdatetime')
def datetimeformatter(value, dateortime):
    """ Date time formatter. """
    return reformat.extract_date_time(value, dateortime)
app.jinja_env.filters['getdatetime'] = datetimeformatter

@app.route('/', methods=['GET'])
def index():
    """ Show index page. """
    return render_template('home.html')

@app.route('/clear', methods=['GET'])
def clear():
    """ Clear previous region searches. """
    searches.clear_previous_regions()
    return redirect("/")

# checklists
@app.route('/checklists', methods=['GET'])
def get_checklist_search():
    """ Show checklist search page. """
    previous = searches.get_previous_regions()
    return render_template('checklists_find.html', previous=previous, page="checklists")

@app.route('/checklists/<string:region>', methods=['GET'])
def get_checklists(region):
    """ Show checklist search results. """
    searches.save_previous_region(region)
    data = service.region_checklists(region)
    return render_template('checklists_results.html', data=data, region=region)

# notables
@app.route('/notables', methods=['GET'])
def get_notables_search():
    """ Show notables search page. """
    previous = searches.get_previous_regions()
    return render_template('notables_find.html', previous=previous, page="notables")

@app.route('/notables/<string:region>', methods=['GET'])
def get_notables(region):
    """ Show notable search results. """
    searches.save_previous_region(region)
    days = str(app.config['DAYS_BACK'])
    data = service.region_notable(region, days)
    return render_template('notables_results.html', data=data, region=region, days=days)

# location
@app.route('/location/<string:region>/<string:location_id>', methods=['GET'])
def get_location(region, location_id):
    """ Show locations page. """
    days = str(app.config['DAYS_BACK'])
    data = service.region_location_obs(location_id, days)
    return render_template('location_results.html', data=data, region=region, days=days)

# species
@app.route('/species/<string:region>/<string:full_name>', methods=['GET'])
def get_species(region, full_name):
    """ Show species page. """
    days = str(app.config['DAYS_BACK'])
    data = service.region_species_obs(region, full_name, days)
    return render_template('species_results.html',
                           data=data, region=region, name=full_name, days=days)

# hotspots
@app.route('/hotspots', methods=['GET'])
def get_hotspots_search():
    """ Show hotspots search page. """
    previous = searches.get_previous_regions()
    return render_template('hotspots_find.html', previous=previous, page="hotspots")

@app.route('/hotspots/<string:region>', methods=['GET'])
def get_hotspots(region):
    """ Show hotspots results page. """
    data = service.region_hotspots(region)
    return render_template('hotspots_results.html', data=data, region=region)

# providers
@app.route('/providers', methods=['GET'])
def get_providers():
    """ Show providers/preferences page. """
    return render_template('providers.html')

#@app.route("/jasmine")
#def jasmine():
#    """ Show test page. """
#    return app.send_static_file('tests/jasmine/SpecRunner.html')

#@app.route("/test")
#def test():
#    """ Show test page. """
#    return "<strong>It's Alive!</strong>"

if __name__ == '__main__':
    app.secret_key = app.config['SECRET_KEY']
    SESSION_TYPE = 'redis'
    Session(app)

    app.run(app.config['IP'], app.config['PORT'])
    app.run(debug=True)
