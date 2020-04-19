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

  @staticmethod
  def search_field(search_field, search_value, merged_data):
    """
    Search fields in merged data
    :param search_field: fields list to be searched
    :param search_value: values of the corresponding fields
    :param merged_data: merged data present from task 1
    :return: Return are the movies fulfilling the searched criteria
    """
    list(search_field)
    list(search_value)
    json_files = Utility.files_in_folder(merged_data)
    result = []
    if search_field == []:
      for file in json_files:
        json_file = merged_data + "/" + file
        with open(json_file, 'rb') as file:  # will close() when we leave this block
          data = json.load(file)
        result.append(data)
    else:
      for file in json_files:
        json_file = merged_data + "/" + file
        with open(json_file, 'rb') as file:  # will close() when we leave this block
          data = json.load(file)
        if all(key in data for key in set(search_field)):
          checkValue = 0
          for i in range(len(search_field)):
            if type(data[search_field[i]]) is list and search_value[i] in data[search_field[i]]:
              pass
            elif str(data[search_field[i]]) == str(search_value[i]):
              pass
            else:
              checkValue = 1
              break
          if checkValue == 0:
            result.append(data)
    return result
