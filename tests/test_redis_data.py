""" Tests Redis data store. """
import sys
import unittest
#sys.path.insert(1, '/home/mrhapi/murmuration')
sys.path.insert(0, '/Users/marcus.hunt/Sites/seebirds_py3')
sys.path.insert(0, '/Users/marcus.hunt/Sites/seebirds_py3/apis')
sys.path.insert(0, '/Users/marcus.hunt/Sites/seebirds_py3/persistence')

print(sys.path)

from time import gmtime, strftime
import redis_instance as connection

db = connection.get_connection()

class RedisTestCase(unittest.TestCase):
    """
    def setUp(self):
    def tearDown(self):
    """

    def test_redis_connection(self):
        db = connection.get_connection()
        self.assertEqual(db, None)

    def test_get_keys(self, pattern='*'):
        """Returns a list of keys matching 'pattern'"""
        db.flushdb()
        db.set('US-MA-025', 'Suffolk (US-MA-025)')
        db.set('GB-ENG-HRT', 'Hertfordshire (GB-ENG-HRT)')
        data = db.execute_command('KEYS', pattern)
        print(data)
        self.assertEqual(data, None)

    def test_get_values_without_hash(self):
        """Returns a list of values for all keys, without using hash"""
        db.flushdb()
        db.set('US-MA-025', 'Suffolk (US-MA-025)')
        db.set('GB-ENG-HRT', 'Hertfordshire (GB-ENG-HRT)')
        args = db.execute_command('KEYS', '*')
        if len(args) > 0:
            data = db.execute_command('MGET', *args)
            print(data)
            self.assertEqual(data, None)
        else:
            print(args)
            self.assertEqual(args, None)

    def test_get_values_from_hash(self):
        """Returns a list of values from a hash """
        db.flushdb()
        db.hset('myhashval', 'US-MA-025', 'Suffolk (US-MA-025)')
        db.hset('myhashval', 'GB-ENG-HRT', 'Hertfordshire (GB-ENG-HRT)')
        data = db.hvals('myhashval')
        print(data)
        self.assertEqual(data, None)

    def test_get_previous_regions_added(self):
        db.flushdb()
        db.set('US-MA-025', 'Suffolk (US-MA-025)')
        db.set('GB-ENG-HRT', 'Hertfordshire (GB-ENG-HRT)')
        data = db.get('US-MA-025')
        self.assertEqual(data.decode('utf-8'), 'Suffolk (US-MA-025)')
