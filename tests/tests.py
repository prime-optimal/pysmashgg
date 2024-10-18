import unittest
import os
import time
import pysmashgg
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

TOURNAMENT_SHOW_EVENT_ID_RESULT = 529399

TOURNAMENT_SHOW_RESULT = {'id': 253044, 'name': 'Smash Summit 10 Online', 'country': 'US', 'state': 'CA', 'city': 'Los Angeles', 'startTimestamp': 1605808800, 'endTimestamp': 1606111200, 'entrants': 68}

class TestClass(unittest.TestCase):
    smash = pysmashgg.SmashGG(os.environ.get('KEY'))

    def test_tournament_show_event_id(self):
        result = self.smash.tournament_show_event_id("smash-summit-10-online", "melee-singles")
        self.assertEqual(result, TOURNAMENT_SHOW_EVENT_ID_RESULT)

    def test_tournament_show(self):
        result = self.smash.tournament_show("smash-summit-10-online")
        self.assertEqual(result, TOURNAMENT_SHOW_RESULT)

    def test_bracket_show_entrants(self):
        result = self.smash.bracket_show_entrants(1401911, 1)
        self.assertIsInstance(result, list)
        self.assertTrue(len(result) > 0)
        self.assertIn('entrantId', result[0])
        self.assertIn('tag', result[0])

    def test_player_show_info(self):
        result = self.smash.player_show_info(1000)
        self.assertEqual(result['tag'], 'Mang0')
        self.assertEqual(result['name'], 'Joseph Marquez')
        self.assertIn('rankings', result)
        self.assertIsInstance(result['rankings'], list)

    def test_event_show_head_to_head(self):
        result = self.smash.event_show_head_to_head(529399, "Mang0", "Zain")
        self.assertIsInstance(result, list)
        self.assertTrue(len(result) > 0)
        self.assertIn('entrant1Name', result[0])
        self.assertIn('entrant2Name', result[0])

    def test_league_show(self):
        result = self.smash.league_show("world-warrior-2024-capcom-pro-tour")
        self.assertIsNotNone(result)
        self.assertIn('id', result)
        self.assertIn('name', result)

if __name__ == '__main__':
    unittest.main()
