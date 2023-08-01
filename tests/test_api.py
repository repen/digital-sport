"""
command
python -m unittest tests/test_api.py
"""
import os
import unittest
from sport import FootballSport
import random
import requests
import sys
# sys.stderr = open("test_error.log", 'a')

TOKEN = os.getenv("TOKEN")

DUMP_FILE = os.getenv("DUMP_FILE")
if DUMP_FILE:
    sys.stderr = open(DUMP_FILE, 'a')

class TestService(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pass

    def setUp(self):
        pass


    def test_02_good_token(self):
        football = FootballSport(TOKEN)
        result = football.live()
        self.assertTrue(isinstance(result, list))

    def test_03_bad_resource(self):
        bad_resource = "bad resource"
        football = FootballSport(TOKEN)

        with self.assertRaises(ValueError):
            football.statistics(bad_resource)

        with self.assertRaises(ValueError):
            football.odds(bad_resource)

        with self.assertRaises(ValueError):
            football.h2h(bad_resource)

    def test_04_good_resource(self):
        football = FootballSport(TOKEN)
        fixtures = football.live()
        random.shuffle(fixtures)

        for fixture in fixtures:
            if fixture['statistics'] != "None":
                match_id = fixture['match_id']
                result = football.odds(match_id)
                self.assertTrue(isinstance(result, list))

                result = football.statistics(match_id)
                self.assertTrue(isinstance(result, list))

                result = football.h2h(match_id)
                self.assertTrue(isinstance(result, list))
                break

    def test_05_read_timeout(self):
        football = FootballSport(TOKEN, requests_params={"timeout":0.01})
        with self.assertRaises(requests.exceptions.ConnectTimeout):
            result = football.live()



    @classmethod
    def tearDownClass(cls):
        pass

def suite():
    suite = unittest.TestSuite()
    suite.addTest(TestService('test_01_live'))
    return suite


if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())
