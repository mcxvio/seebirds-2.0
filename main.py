"""
Main entry to application.
"""
from apis.ebird import recent
from apis.ebird import reformat
from apis.ebird import regions as searches
from flask import Flask, session
from flask import render_template
from flask import redirect
from flask import request
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

# checklists
@app.route('/checklists', methods=['GET'])
def get_checklist_search():
    """ Show checklist search page. """
    return render_template('checklists_find.html')

@app.route('/checklists/<string:region>', methods=['GET'])
def get_checklists(region):
    """ Show checklist search results. """
    searches.save_previous_region(region)
    data = recent.region_checklists(region)
    return render_template('checklists_results.html', data=data, region=region)

# notables
@app.route('/notables', methods=['GET'])
def get_notables_search():
    """ Show notables search page. """
    return render_template('notables_find.html')

@app.route('/notables/<string:region>', methods=['GET'])
def get_notables(region):
    """ Show notable sightings page. """
    searches.save_previous_region(region)
    data = recent.region_notable(region)
    return render_template('notables_results.html', data=data, region=region)

# location
@app.route('/location/<string:region>/<string:location_id>', methods=['GET'])
def get_location(region, location_id):
    """ Show locations page. """
    data = recent.hotspot_obs(location_id)
    return render_template('location_results.html', data=data, region=region)

# species
@app.route('/species/<string:region>/<string:full_name>', methods=['GET'])
def get_species(region, full_name):
    """ Show species page. """
    data = recent.region_species_obs(region, full_name)
    return render_template('species_results.html', data=data, region=region, name=full_name)

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

#@app.route('/outdoors')
#def outdoors():
#    """ Show outdoors page. """
#    return app.send_static_file('outdoors.html')

# previous regions searched
#@app.route('/previous_regions/<string:to_page>', methods=['GET'])
#def get_previous_region_searches(to_page):
#    """ Show previous regions searched for. """
#    data = searches.get_previous_regions()
#    page = 'submissions' if to_page == 'checklists' else 'sightings'
#    return render_template('previous_regions.html', data=data, page=page)

#@app.route('/clear_previous_regions', methods=['GET'])
#def clear_previous_region_searches():
#    searches.clear_previous_regions()
#    return redirect("/")


if __name__ == '__main__':
    app.secret_key = app.config['SECRET_KEY']
    SESSION_TYPE = 'redis'
    Session(app)

    app.run(app.config['IP'], app.config['PORT'])
    app.run(debug=True)
