""" Tests for eBird API """
import sys
import unittest
#sys.path.insert(1, '/home/mrhapi/murmuration')
sys.path.insert(0, '/Users/marcus.hunt/Sites/seebirds_py3')
sys.path.insert(0, '/Users/marcus.hunt/Sites/seebirds_py3/apis')

print(sys.path)

from apis.ebird import recent
from apis.ebird import reformat
from time import gmtime, strftime

class EbirdTestCase(unittest.TestCase):

    """
    def setUp(self):

    def tearDown(self):
    """

    def test_extract_type_from_region(self):
        """ Extract region type from selected region """
        result = reformat.extract_region_code('Suffolk (US-MA-025)')
        self.assertEqual(result, 'US-MA-025')

    def test_extract_sub_from_sub_code(self):
        """ Extract subregion from a subregion code (fix bug) """
        result = reformat.extract_region_code('US-MA-025')
        self.assertEqual(result, 'US-MA-025')

    def test_region_is_country(self):
        """ Region is a country? """
        result = reformat.extract_region_type('US-')
        self.assertEqual(result, 'country')

    def test_region_is_state(self):
        """ Region is a state? """
        result = reformat.extract_region_type('US-MA')
        self.assertEqual(result, 'subnational1')

    def test_region_is_county(self):
        """ Region is a county? """
        result = reformat.extract_region_type('US-MA-025')
        self.assertEqual(result, 'subnational2')

    def test_invalid_region_for_obs(self):
        """ Invalid region for a region observation? """
        response = recent.region_obs('XX-XX-000')
        print("test_invalid_region_obs response = ", response)
        self.assertEqual(str(response), "[{'obsDt': '', 'checklists': []}, {'chkCount': 0}]")

    def test_invalid_region_for_notable(self):
        """ Invalid region for a region notable observation? """
        response = recent.region_notable('subregion')
        print("test_invalid_region_notable response = ", response)
        self.assertEqual(str(response), '[]')

    def test_invalid_region_for_species(self):
        """ Invalid region for a region species observation? """
        response = recent.region_species_obs('subregion', 'Aix sponsa')
        print("test_invalid_region_species_obs response = ", response)
        self.assertEqual(str(response), '[]')

    def test_invalid_hotspot_for_obs(self):
        """ Invalid hotspot for a hotspot observation? """
        response = recent.hotspot_obs('LocX')
        print("test_invalid_hotspot_obs response = ", response)
        self.assertEqual(str(response), '[]')

    def test_invalid_spp_for_species(self):
        """ Invalid species for a region species observation? """
        response = recent.region_species_obs('US-MA-025', 'Sci name')
        print("test_invalid_region_species_obs response = ", response)
        self.assertEqual(str(response), "[{'errorCode': 'error.data.unknown_species',"
                         + " 'errorMsg': 'Unknown species: Sci name'}]")

    def test_invalid_regspp_for_regspp(self):
        """ Invalid region and species for region species observation? """
        response = recent.region_species_obs('subnational', 'Sci name')
        print("test_invalid_region_species_obs response = ", response)
        self.assertEqual(str(response), "[{'errorCode': 'error.data.unknown_species',"
                         + " 'errorMsg': 'Unknown species: Sci name'}]")

    def test_datetime_formatting_options(self):
        """" Datetime returned when passing datetime and format parameter """
        dateortime = 'da'
        value = "2017-11-21 17:07"
        response = reformat.extract_date_time(value, dateortime)
        self.assertEqual(response, "Tuesday 21 November")


if __name__ == '__main__':
    unittest.main()
