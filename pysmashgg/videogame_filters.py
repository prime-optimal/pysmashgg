"""Filters for video game related queries."""

def get_videogame_id_filter(response):
    """Filter for the get_videogame_id function"""
    if 'data' not in response or 'videogames' not in response['data']:
        return None
    
    nodes = response['data']['videogames']['nodes']
    if not nodes:
        return None
        
    # Return the first matching game's ID
    return nodes[0]['id']

def show_by_videogame_filter(response):
    """Filter for the show_by_videogame function"""
    if 'data' not in response or 'tournaments' not in response['data']:
        return None

    if response['data']['tournaments']['nodes'] is None:
        return None

    tournaments = []

    for node in response['data']['tournaments']['nodes']:
        cur_tournament = {}
        cur_tournament['id'] = node['id']
        cur_tournament['name'] = node['name']
        cur_tournament['slug'] = node['slug']
        cur_tournament['entrants'] = node['numAttendees']
        cur_tournament['country'] = node['countryCode']
        cur_tournament['state'] = node['addrState']
        cur_tournament['city'] = node['city']
        cur_tournament['startTimestamp'] = node['startAt']
        cur_tournament['endTimestamp'] = node['endAt']
        
        # Add event information
        events = []
        for event in node['events']:
            if event['videogame'] is not None:  # Only include events for the specified game
                events.append({
                    'id': event['id'],
                    'name': event['name'],
                    'entrants': event['numEntrants']
                })
        cur_tournament['events'] = events

        tournaments.append(cur_tournament)

    return tournaments
