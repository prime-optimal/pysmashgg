"""Tournament-related API functions for the pysmashgg library.

This module provides functions for interacting with tournament-related endpoints
of the smash.gg API, including searching and retrieving tournament information.
Recent changes:
- Added date filtering for tournament searches by game, defaulting to next week
"""

from pysmashgg import filters, videogame_filters
from pysmashgg.t_queries import *
from pysmashgg.api import run_query
from datetime import datetime, timedelta
import time

# HELPER FUNCTIONS

def get_player_id(event_id, player_name, header, auto_retry):
    """Get playerId at an event"""
    variables = {"eventId": event_id, "name": player_name}
    response = run_query(PLAYER_ID_QUERY, variables, header, auto_retry)
    data = filters.player_id_filter(response, player_name)
    return data

def get_entrant_id(event_id, player_name, header, auto_retry):
    """Get entrantId at an event"""
    variables = {"eventId": event_id, "name": player_name}
    response = run_query(ENTRANT_ID_QUERY, variables, header, auto_retry)
    data = response['data']['event']['entrants']['nodes'][0]['id']
    return data

def get_event_id(tournament_name, event_name, header, auto_retry):
    """Get an eventId from a tournament"""
    variables = {"tourneySlug": tournament_name}
    response = run_query(EVENT_ID_QUERY, variables, header, auto_retry)
    data = filters.event_id_filter(response, event_name)
    return data

# TOURNAMENT FUNCTIONS

def show(tournament_name, header, auto_retry):
    """Get metadata for a tournament"""
    variables = {"tourneySlug": tournament_name}
    response = run_query(SHOW_QUERY, variables, header, auto_retry)
    data = filters.show_filter(response)
    return data

def show_with_brackets(tournament_name, event_name, header, auto_retry):
    """Get metadata for a tournament with specific brackets"""
    variables = {"tourneySlug": tournament_name}
    response = run_query(SHOW_WITH_BRACKETS_QUERY, variables, header, auto_retry)
    data = filters.show_with_brackets_filter(response, event_name)
    return data

def show_with_brackets_all(tournament_name, header, auto_retry):
    """Get metadata for a tournament with all brackets"""
    variables = {"tourneySlug": tournament_name}
    response = run_query(SHOW_WITH_BRACKETS_QUERY, variables, header, auto_retry)
    data = filters.show_with_brackets_all_filter(response)
    return data

def show_events(tournament_name, header, auto_retry):
    """Get all events from a tournament"""
    variables = {"tourneySlug": tournament_name}
    response = run_query(SHOW_EVENTS_QUERY, variables, header, auto_retry)
    data = filters.show_events_filter(response)
    return data

def show_sets(tournament_name, event_name, page_num, header, auto_retry):
    """Get all sets from an event"""
    event_id = get_event_id(tournament_name, event_name, header, auto_retry)
    variables = {"eventId": event_id, "page": page_num}
    response = run_query(SHOW_SETS_QUERY, variables, header, auto_retry)
    data = filters.show_sets_filter(response)
    return data
            
def show_entrants(tournament_name, event_name, page_num, header, auto_retry):
    """Get all entrants from a specific event"""
    event_id = get_event_id(tournament_name, event_name, header, auto_retry)
    variables = {"eventId": event_id, "page": page_num}
    response = run_query(SHOW_ENTRANTS_QUERY, variables, header, auto_retry)
    data = filters.show_entrants_filter(response)
    return data

def show_event_brackets(tournament_name, event_name, header, auto_retry):
    """Get all event bracket IDs, names, and slugs"""
    variables = {"tourneySlug": tournament_name}
    response = run_query(SHOW_EVENT_BRACKETS_QUERY, variables, header, auto_retry)
    data = filters.show_events_brackets_filter(response, event_name)
    return data

def show_all_event_brackets(tournament_name, header, auto_retry):
    """Get all event brackets for a tournament"""
    variables = {"tourneySlug": tournament_name}
    response = run_query(SHOW_EVENT_BRACKETS_QUERY, variables, header, auto_retry)
    data = filters.show_all_event_brackets_filter(response)
    return data

def show_entrant_sets(tournament_name, event_name, entrant_name, header, auto_retry):
    """Get all sets for a specific entrant"""
    event_id = get_event_id(tournament_name, event_name, header, auto_retry)
    entrant_id = get_entrant_id(event_id, entrant_name, header, auto_retry)
    variables = {"eventId": event_id, "entrantId": entrant_id, "page": 1}
    response = run_query(SHOW_ENTRANT_SETS_QUERY, variables, header, auto_retry)
    data = filters.show_entrant_sets_filter(response)
    return data

def show_head_to_head(tournament_name, event_name, entrant1_name, entrant2_name, header, auto_retry):
    """Get head to head results for two entrants"""
    event_id = get_event_id(tournament_name, event_name, header, auto_retry)
    entrant1_id = get_entrant_id(event_id, entrant1_name, header, auto_retry)
    variables = {"eventId": event_id, "entrantId": entrant1_id, "page": 1}
    response = run_query(SHOW_ENTRANT_SETS_QUERY, variables, header, auto_retry)
    data = filters.show_head_to_head_filter(response, entrant2_name)
    return data

def show_event_by_game_size_dated(num_entrants, videogame_id, after, before, page_num, header, auto_retry):
    """Get all events of a minimum size between two timestamps"""
    variables = {"videogameId": videogame_id, "after": after, "before": before, "page": page_num}
    response = run_query(SHOW_EVENT_BY_GAME_SIZE_DATED_QUERY, variables, header, auto_retry)
    data = filters.show_event_by_game_size_dated_filter(response, num_entrants, videogame_id)
    return data

def show_lightweight_results(tournament_name, event_name, page_num, header, auto_retry):
    """Get basic results (name, id, placement) for an event"""
    event_id = get_event_id(tournament_name, event_name, header, auto_retry)
    variables = {"eventId": event_id, "page": page_num}
    response = run_query(SHOW_LIGHTWEIGHT_RESULTS_QUERY, variables, header, auto_retry)
    data = filters.show_lightweight_results_filter(response)
    return data

def show_by_country(country_code, page_num, header, auto_retry):
    """Get tournaments by country"""
    variables = {"countryCode": country_code, "page": page_num}
    response = run_query(SHOW_BY_COUNTRY_QUERY, variables, header, auto_retry)
    data = filters.show_by_country_filter(response)
    return data

def show_by_state(state_code, page_num, header, auto_retry):
    """Get tournaments by US state"""
    variables = {"state": state_code, "page": page_num}
    response = run_query(SHOW_BY_STATE_QUERY, variables, header, auto_retry)
    data = filters.show_by_state_filter(response)
    return data

def show_by_radius(coordinates, radius, page_num, header, auto_retry):
    """Get tournaments within a radius of coordinates"""
    variables = {"coordinates": coordinates, "radius": radius, "page": page_num}
    response = run_query(SHOW_BY_RADIUS_QUERY, variables, header, auto_retry)
    data = filters.show_by_radius_filter(response)
    return data

def show_players_by_sponsor(tournament_name, sponsor, header, auto_retry):
    """Get players by sponsor at a tournament"""
    variables = {"slug": tournament_name, "sponsor": sponsor}
    response = run_query(SHOW_PLAYERS_BY_SPONSOR, variables, header, auto_retry)
    data = filters.show_players_by_sponsor_filter(response)
    return data

def show_by_owner(owner, page_num, header, auto_retry):
    """Get tournaments by owner ID"""
    variables = {"ownerId": owner, "page": page_num}
    response = run_query(SHOW_BY_OWNER_QUERY, variables, header, auto_retry)
    data = filters.show_by_owner_filter(response)
    return data

def get_videogame_id(game_name, header, auto_retry):
    """Get the ID for a video game by its name"""
    variables = {"name": game_name}
    response = run_query(GET_VIDEOGAME_ID_QUERY, variables, header, auto_retry)
    data = videogame_filters.get_videogame_id_filter(response)
    return data

def show_by_videogame(videogame_id, page_num, header, auto_retry, after=None, before=None):
    """Shows a list of tournaments for a specific video game
    
    Args:
        videogame_id: The ID of the video game to search for
        page_num: The page number of results to return
        header: The authorization header for the API
        auto_retry: Whether to automatically retry failed requests
        after: Optional Unix timestamp for the earliest tournament start date (defaults to current time)
        before: Optional Unix timestamp for the latest tournament start date (defaults to 7 days from now)
    """
    # Set default date range to next week if not provided
    if after is None:
        after = int(time.time())  # Current time
    if before is None:
        before = int((datetime.now() + timedelta(days=7)).timestamp())  # 7 days from now

    variables = {
        "videogameId": videogame_id,
        "page": page_num,
        "after": after,
        "before": before
    }
    response = run_query(SHOW_BY_VIDEOGAME_QUERY, variables, header, auto_retry)
    data = videogame_filters.show_by_videogame_filter(response)
    return data
