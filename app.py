from apis.ebird import recent
from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return 'Welcome to Murmuation :: worldwide birding data!'

@app.route('/location/')
def checklists():
    response = recent.get_location_obs()

    return response
