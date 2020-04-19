import unittest
from utils.Utility import Utility
from config.settings import api_key, OMDb_url, merged_data

class UtilityTest(unittest.TestCase):

  def test_files_in_folder_1(self):
    actual = Utility.files_in_folder("./movie-metadata-service/movies")
    expected = ['11528860.json', '3532674.json', '5979300.json', '11043689.json']
    self.assertEqual(expected, actual)

  def test_files_in_folder_2(self):
    self.assertRaises(FileNotFoundError,Utility.files_in_folder, "testtt" )

  def test_search_json_files_1(self):
    data, actual = Utility.search_json_file(11043689,"./movie-metadata-service/movies")
    self.assertFalse(actual)

  def test_search_json_files_2(self):
    data, actual = Utility.search_json_file("tt0076759","./movie-metadata-service/movies")
    self.assertTrue(actual)

  def test_search_json_files_3(self):
    data, actual = Utility.search_json_file("1104368","./movie-metadata-service/movies")
    self.assertIsNone(data)

  def test_search_omdb_data_1(self):
    data = Utility.search_omdb_data("tt0076759", "http://www.omdbapi.com", "vbh")
    self.assertEqual("Invalid API key!", data['Error'])

  def test_search_omdb_data_2(self):
    data = Utility.search_omdb_data("tt0076759", OMDb_url, api_key )
    self.assertEqual("tt0076759", data['imdbID'])

  def test_getting_moving_data_1(self):
    data = Utility.getting_moving_data(11043689, "./movie-metadata-service/movies", OMDb_url, api_key)
    self.assertEqual(11043689,data['id'])

  def test_getting_moving_data_2(self):
    data = Utility.getting_moving_data("tt0076759", "./movie-metadata-service/movies", OMDb_url, api_key)
    self.assertEqual("tt0076759", data['imdbID'])

  def test_getting_moving_data_3(self):
    data = Utility.getting_moving_data(1104368, "./movie-metadata-service/movies", OMDb_url, api_key)
    self.assertEqual("Incorrect IMDb ID.", data['Error'])

  def test_search_field_1(self):
    data = Utility.search_field([], [], merged_data)
    json_files = Utility.files_in_folder(merged_data)
    self.assertEqual(len(json_files),len(data))

  def test_search_field_2(self):
    data = Utility.search_field(["Writer","Year"], ["Lime Lucas","1977"], merged_data)
    self.assertEqual(0,len(data))

if __name__=='__main__':
    unittest.main()
