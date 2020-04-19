from flask import Flask
from utils.Utility import Utility
from flask import request
from config.settings import movie_metadata, OMDb_url, api_key, merged_data
import json

app = Flask(__name__)


@app.route('/api/movies/<id>')
def getting_movie_data(id):
    data = Utility.getting_moving_data(id, movie_metadata, OMDb_url, api_key)
    if 'imdbID' in data.keys():
      with open(merged_data + "/" + data['imdbID'] + ".json", 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    return data


@app.route('/api/movies')
def search():
    search_field = []
    search_value = []
    for key in request.args:
        search_field.append(key)
        search_value.append(request.args[key])
    data = Utility.search_field(search_field, search_value, merged_data)
    return json.dumps(data)


@app.route('/')
def hello_world():
  return 'hello!'


@app.errorhandler(404)
def not_found(e):
  return {"error":"404!! Error"}
