""" Tests for eBird API """
import sys
import unittest
sys.path.insert(0, '/Users/marcus.hunt/Sites/seebirds_py3_api')
sys.path.insert(0, '/Users/marcus.hunt/Sites/seebirds_py3_api/apis')

print(sys.path)

import json
import ijson

from time import gmtime, strftime
from apis.ebird import requester
from apis.ebird import service
from apis.ebird import reformat

class EbirdTestCase(unittest.TestCase):

    """
    def setUp(self):

    def tearDown(self):
    """
    def test_get_ebird_key(self):
        """ Get the eBird key for API 2.0 """
        data = ''
        with open('keys.json') as json_data_file:
            data = json.load(json_data_file)
        print(str(data['ebird_key']))
        self.assertEqual(str(data), '')

    def test_valid_region_for_obs(self):
        """ Valid region for a region observation, 2.0 API """
        response = service.region_checklists('US-MA-025')
        print("test_valid_region_for_obs response = ", response)
        self.assertEqual(str(response), '')

    def test_valid_region_for_species(self):
        """ Valid region for a region species observation? """
        response = service.region_species_code_obs('GB-SCT', 'goleag', '5')
        sys.stdout.write("test_valid_region_species_obs response = " + str(response))
        self.assertEqual(str(response), '')

    def test_extinct_species_from_json(self):
        """ View all the extinct species and year of extinction. """
        response = ""
        with open('data_taxaspecies.json') as json_data_file:

            data = ijson.items(json_data_file, 'response.taxa.item')
            species = (s for s in data if s.get("extinct") is not None and s["extinct"])

            response = list(species)
            print(response)
        self.assertEqual(len(response), 0)

    def test_family_species_from_json(self):
        """ Valid family name to retrieve species. """
        response = ""
        with open('data_taxaspecies.json') as json_data_file:

            data = ijson.items(json_data_file, 'response.taxa.item')
            species = (s for s in data if s.get("familyComName") is not None
                       and s["familyComName"] == 'Ostriches')

            response = list(species)
            print(len(response))
        self.assertGreater(len(response), 0)

    def test_family_species_from_stream(self):
        """ Valid family name to retrieve species via stream. """
        stream = []
        species = ""
        order = ""
        family = "Ostriches"
        with open('data_taxaspecies.json') as json_data_file:

            parser = ijson.parse(json_data_file)
            stream.append('<spp>')
            for prefix, event, value in parser:
                if (prefix, event) == ('response.taxa.item.comName', 'string'):
                    species = value
                elif (prefix, event) == ('response.taxa.item.order', 'string'):
                    order = value
                elif (prefix, event) == ('response.taxa.item.familyComName', 'string') and value == family:
                    stream.append('<%s>' % species)
                    stream.append('<%s>' % value)
                    stream.append('<%s>' % order)
                #elif 'Ostriches' in prefix:
                #    stream.append('<object name="%s"/>' % value)
                #elif prefix.endswith('.familyComName'):
                #else:
                #    if value == 'Ostriches':
                #        print(prefix)
                #        print(event)
                #        stream.append('<object name="%s"/>' % value)
                #elif (prefix, event) == ('response.taxa.item.%s' % value, 'end_map'):
                #    stream.append('</%s>' % value)
            stream.append('</spp>')

            """
            data = ijson.items(json_data_file, 'response.taxa.item')
            species = (s for s in data if s.get("familyComName") is not None
                       and s["familyComName"] == 'Ostriches')

            response = list(species)
            print(len(response))
            """
        print(''.join(stream))
        print(len(stream))
        self.assertEqual(len(stream), 0)

    def test_order_species_from_stream(self):
        """ Valid family name to retrieve species via stream. """
        stream = []
        search = "Struthioniformes"
        species = ""
        order = ""
        family = ""
        with open('data_taxaspecies.json') as json_data_file:

            parser = ijson.parse(json_data_file)
            stream.append('<spp>')
            for prefix, event, value in parser:
                if (prefix, event) == ('response.taxa.item.comName', 'string'):
                    species = value
                elif (prefix, event) == ('response.taxa.item.familyComName', 'string'):
                    family = value
                elif (prefix, event) == ('response.taxa.item.order', 'string'):
                    order = value
                if order == search:
                    stream.append('<%s>' % species)
                    stream.append('<%s>' % family)
                    stream.append('<%s>' % order)
            stream.append('</spp>')

        print(''.join(stream))
        print(len(stream))
        self.assertEqual(len(stream), 0)

    #
    # Invalid tests.
    #
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
        response = service.region_checklists('XX-XX-000')
        print("test_invalid_region_obs response = ", response)
        self.assertEqual(str(response), "[{'obsDt': '', 'checklists': []}, {'chkCount': 0}]")

    def test_invalid_region_for_notable(self):
        """ Invalid region for a region notable observation? """
        response = service.region_notable('subregion', '5')
        print("test_invalid_region_notable response = ", response)
        self.assertEqual(str(response), '[]')

    def test_invalid_region_for_species(self):
        """ Invalid region for a region species observation? """
        response = service.region_species_code_obs('subregion', 'rocpig1', '5')
        print("test_invalid_region_species_obs response = ", response)
        self.assertEqual(str(response), '[]')

    def test_invalid_hotspot_for_obs(self):
        """ Invalid hotspot for a hotspot observation? """
        response = service.region_hotspots('LocX')
        print("test_invalid_hotspot_obs response = ", response)
        self.assertEqual(str(response), '[]')

    def test_invalid_spp_for_species(self):
        """ Invalid species for a region species observation? """
        response = service.region_species_code_obs('US-MA-025', 'Sci name', '5')
        print("test_invalid_region_species_obs response = ", response)
        self.assertEqual(str(response), "[{'errorCode': 'error.data.unknown_species',"
                         + " 'errorMsg': 'Unknown species: Sci name'}]")

    def test_invalid_regspp_for_regspp(self):
        """ Invalid region and species for region species observation? """
        response = service.region_species_code_obs('subnational', 'Sci name', '5')
        print("test_invalid_region_species_obs response = ", response)
        self.assertEqual(str(response), "[{'errorCode': 'error.data.unknown_species',"
                         + " 'errorMsg': 'Unknown species: Sci name'}]")

    def test_datetime_format_options(self):
        """" Datetime returned when passing datetime and format parameter """
        dateortime = 'da'
        value = "2017-11-21 17:07"
        response = reformat.extract_date_time(value, dateortime)
        self.assertEqual(response, "Tuesday 21 November")


if __name__ == '__main__':
    unittest.main()
