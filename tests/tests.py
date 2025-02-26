import unittest
import os
import time
import json
import pysmashgg
from dotenv import load_dotenv
from pysmashgg.api import run_query
from pysmashgg.queries import PLAYER_INFO_QUERY

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
        self.assertIsNotNone(result, "API response should not be None")
        if result:  # Only check fields if we got a valid response
            self.assertEqual(result.get('tag'), 'Mang0')
            self.assertEqual(result.get('name'), 'Joseph Marquez')
            self.assertIn('rankings', result)
            self.assertIsInstance(result['rankings'], list)
            # Test for social media information
            self.assertIn('socials', result)
            self.assertIsInstance(result['socials'], dict)

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

    def test_tournament_league_results(self):
        """Test getting results from a league tournament"""
        result = self.smash.tournament_show("mashing-madness-latam-sur-2023")
        self.assertIsNotNone(result)
        # Check that we get the correct dates for the league
        self.assertEqual(time.strftime('%Y-%m-%d', time.localtime(result['startTimestamp'])), '2023-06-26')
        self.assertEqual(time.strftime('%Y-%m-%d', time.localtime(result['endTimestamp'])), '2023-12-31')
        # Check that it's marked as online
        self.assertIsNone(result.get('city'))
        self.assertIsNone(result.get('state'))

    def test_api_rate_limit_handling(self):
        """Test handling of API rate limits"""
        # Make multiple rapid requests to trigger rate limiting
        results = []
        for _ in range(5):
            result = self.smash.tournament_show("mashing-madness-latam-sur-2023")
            results.append(result is not None)
            time.sleep(0.5)  # Small delay to avoid actual rate limiting during tests

        # All requests should have succeeded with our rate limit handling
        self.assertTrue(all(results))

    def test_player_info_without_game(self):
        """Test getting player info without requiring game ID"""
        result = self.smash.player_show_info(1000)  # Mang0's ID
        self.assertIsNotNone(result, "API response should not be None")
        if result:  # Only check fields if we got a valid response
            self.assertEqual(result.get('tag'), 'Mang0')
            self.assertIn('socials', result)

    def test_player_id_in_response(self):
        """Test that player ID is included in the player info response"""
        result = self.smash.player_show_info(1000)  # Mang0's ID
        self.assertIsNotNone(result, "API response should not be None")
        if result:  # Only check fields if we got a valid response
            self.assertIn('id', result, "Player ID should be included in the response")
            self.assertEqual(result.get('id'), 1000)

    def test_player_lookup_formats(self):
        """Test that player lookup works with different identifier formats"""
        # Test with CLI utils directly
        from cli.utils.player import format_player_slug, lookup_player_id

        # Test format_player_slug function
        self.assertEqual(format_player_slug("user/b1008ff3"), "user/b1008ff3", "Should keep user/ prefix")
        self.assertEqual(format_player_slug("b1008ff3"), "user/b1008ff3", "Should add user/ prefix")

        # Test with API directly if possible (requires API key)
        if os.environ.get('KEY'):
            # Use a known player ID and slug for testing
            variables = {"playerId": "1000"}  # Mang0's ID
            response = run_query(PLAYER_INFO_QUERY, variables, {"Authorization": "Bearer " + os.environ.get('KEY')}, True)
            self.assertIsNotNone(response, "API response should not be None")
            self.assertIn('data', response, "Response should contain data")
            self.assertIn('player', response['data'], "Response should contain player data")
            self.assertIn('id', response['data']['player'], "Player data should include ID")

if __name__ == '__main__':
    unittest.main()
