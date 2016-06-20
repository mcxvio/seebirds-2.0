import sys
sys.path.insert(1, '/home/mrhapi/murmuration')

print(sys.path)

from apis.ebird import recent
from apis.ebird import reformat
import unittest

class EbirdTestCase(unittest.TestCase):

    '''
    def setUp(self):

    def tearDown(self):
    '''

    def test_extract_region_type_from_selected_region(self):
        result = reformat.extractRegionCode('Suffolk (US-MA-025)')
        self.assertEqual(result, 'US-MA-025')

    def test_region_is_country(self):
        result = reformat.extractRegionType('US-')
        self.assertEqual(result, 'country')

    def test_region_is_state(self):
        result = reformat.extractRegionType('US-MA')
        self.assertEqual(result, 'subnational1')

    def test_region_is_county(self):
        result = reformat.extractRegionType('US-MA-025')
        self.assertEqual(result, 'subnational2')

    def test_invalid_region_for_region_obs(self):
        response = recent.region_obs('rtype', 'subregion')
        print("test_invalid_region_obs response = ", response)
        self.assertEqual(response, '[]')

    def test_invalid_region_for_region_notable(self):
        response = recent.region_notable('rtype', 'subregion')
        print("test_invalid_region_notable response = ", response)
        self.assertEqual(response, '[]')

    def test_invalid_hotspot_for_hotspot_obs(self):
        response = recent.hotspot_obs('LocX')
        print("test_invalid_hotspot_obs response = ", response)
        self.assertEqual(response, '[]')

    def test_invalid_region_for_region_species_obs(self):
        response = recent.region_species_obs('rtype', 'subregion', 'Aix sponsa')
        print("test_invalid_region_species_obs response = ", response)
        self.assertEqual(response, '[]')

    def test_invalid_species_for_region_species_obs(self):
        response = recent.region_species_obs('subnational2', 'US-MA-025', 'Sci name')
        print("test_invalid_region_species_obs response = ", response)
        self.assertEqual(response, '[]')

    def test_invalid_region_and_species_for_region_species_obs(self):
        response = recent.region_species_obs('rtype', 'subnational', 'Sci name')
        print("test_invalid_region_species_obs response = ", response)
        self.assertEqual(response, '[]')


if __name__ == '__main__':
    unittest.main()
