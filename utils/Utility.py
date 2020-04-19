from os import listdir
import json
import requests



class Utility:

  @staticmethod
  def files_in_folder(folder):
    """
    list all the files in folder
    :param folder: folder path
    :return: list of files in folder
    """
    try:
      json_files = listdir(folder)
      return json_files
    except FileNotFoundError:
      raise FileNotFoundError("File does not exist")
    except:
      print("Other error")


  @staticmethod
  def search_json_file(id, movie_metadata):
    """
    seacrh internal data for required id
    :param id: is an alphanumeric value that can either refer to OMDb movie ids or our internal ids.
    :param movie_metadata: path of internal data
    :return: return dict of movie with required id
    """
    json_files = Utility.files_in_folder(movie_metadata)
    for file in json_files:
      json_file = movie_metadata + "/" + file
      with open(json_file , 'rb') as file:  # will close() when we leave this block
        data = json.load(file)
      if str(data['id']) == str(id):
        return data, False
      elif str(data['imdbId']) == str(id):
        return data, True
    return None, True

  @staticmethod
  def search_omdb_data(id, OMDb_url, api_key):
    PARAMS = {'i': id, 'apikey': api_key, 'plot': 'full'}
    data = requests.get(url=OMDb_url, params=PARAMS) #request omdb server to get data for required imdbID
    return data.json() #return json

  @staticmethod
  def combine_json(meta_json, omdb_json):
    """
    Combine two JSON as per requirement
    :param meta_json: internal data JSON
    :param omdb_json: omdb data JSON
    :return: merged json of both JSON
    """
    meta_json.update(omdb_json)
    meta_json.pop('title')
    meta_json.pop('description')
    meta_json.pop('duration')
    meta_json.pop('imdbId')
    meta_json['Ratings'].append({'userrating': meta_json['userrating']})
    meta_json.pop('userrating')
    meta_json['Director'] = omdb_json['Director'].split(',')
    meta_json['Writer'] = omdb_json['Writer'].split(',')
    meta_json['Actors'] = omdb_json['Actors'].split(',')
    return meta_json



  @staticmethod
  def getting_moving_data(id, movie_metadata, OMDb_url, api_key):
    meta_json, flag = Utility.search_json_file(id, movie_metadata)
    if meta_json is None:
      return Utility.search_omdb_data(id, OMDb_url, api_key)
    if flag:
      omdb_json = Utility.search_omdb_data(id, OMDb_url, api_key)
    else:
      omdb_json = Utility.search_omdb_data(meta_json['imdbId'], OMDb_url, api_key)
    data = Utility.combine_json(meta_json, omdb_json)
    return data
