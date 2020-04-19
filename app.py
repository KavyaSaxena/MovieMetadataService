from flask import Flask
from utils.Utility import Utility
from config.settings import movie_metadata, OMDb_url, api_key
import json

app = Flask(__name__)


@app.route('/api/movies/<id>')
def getting_movie_data(id):
    data = Utility.getting_moving_data(id, movie_metadata, OMDb_url, api_key)
    return data
