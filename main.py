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

app = Flask(__name__, static_folder='', static_url_path='')
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

    if full_name.find("(") > 0:
        species_code = full_name[full_name.rfind("(")+1:full_name.rfind(")")]
    else:
        species_code = full_name

    searches.save_previous_region(region)
    data = service.region_species_code_obs(region, species_code, days)
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

# taxa
@app.route('/taxa', methods=['GET'])
def get_taxa_search():
    """ Show taxa search page. """
    previous = searches.get_previous_species()
    return render_template('taxa_find.html', previous=previous, page="taxa")

@app.route('/taxa/<string:species>/<string:family>/<string:order>', methods=['GET'])
def get_taxa(species, family, order):
    """ Show taxa results page. """
    previous = searches.get_previous_regions()
    name = species[0:species.rfind("(")]
    code = species[species.rfind("(")+1:species.rfind(")")]
    searches.save_previous_species(species, family, order)
    return render_template('taxa_results.html', name=name, code=code, family=family, order=order,
                           previous=previous, page="species")

# taxonomy
@app.route('/family/<string:family>', methods=['GET'])
def get_family_species(family):
    """ Show taxa family results page. """
    data = service.family_species(family)
    return render_template('taxa_results_family.html', data=data)

@app.route('/order/<string:order>', methods=['GET'])
def get_order_species(order):
    """ Show taxa order results page. """
    data = service.order_species(order)
    return render_template('taxa_results_order.html', data=data)

@app.route('/extinct', methods=['GET'])
def get_extinct_species():
    """ View all the extinct species and year of extinction. """
    data = service.extinct_species_all()
    return render_template('extinct_results.html', data=data)

# data
@app.route('/data_taxaspecies', methods=['GET'])
def get_taxa_data():
    """ Return the species data from root, enabling both typeahead and json file searches. """
    return app.send_static_file('data_taxaspecies.json')

@app.route('/data_subnationals', methods=['GET'])
def get_region_data():
    """ Return the region data from root, for consistency with species data. """
    return app.send_static_file('data_subnationals2.json')

# providers
@app.route('/providers', methods=['GET'])
def get_providers():
    """ Show providers/preferences page. """
    return render_template('providers.html')

#@app.route("/jasmine")
#def jasmine():
#    """ Show test page. """
#    return app.send_static_file('tests/jasmine/SpecRunner.html')

if __name__ == '__main__':
    app.secret_key = app.config['SECRET_KEY']
    SESSION_TYPE = 'redis'
    Session(app)

    app.run(app.config['IP'], app.config['PORT'])
    app.run(debug=True)
