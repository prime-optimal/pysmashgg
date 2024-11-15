# Player-specific filters

def player_id_filter(response, player_name):
    """Filter for the player_id function"""
    if response['data']['event']['entrants']['nodes'] is None:
        return

    for node in response['data']['event']['entrants']['nodes'][0]['participants']:
        if node['gamerTag'].lower() == player_name.lower():
            player_id = node['player']['id']
        elif (node['participants'][0]['gamerTag'].split("|")[-1]).lower() == player_name.lower():
            player_id = node['player']['id']

    return player_id

def player_show_info_filter(response):
    """Filter for the get_info function"""
    if not response or 'data' not in response:
        return None
    if response['data']['player'] is None:
        return None
    if response['data']['player']['user'] is None:
        return None

    player = {}
    player['tag'] = response['data']['player']['gamerTag']
    player['name'] = response['data']['player']['user']['name']

    # Process social media authorizations
    player['socials'] = {}
    if response['data']['player']['user'].get('authorizations'):
        for auth in response['data']['player']['user']['authorizations']:
            if auth['type'] and auth['externalUsername']:
                player['socials'][auth['type'].lower()] = auth['externalUsername']

    if response['data']['player']['user']['location'] is not None:
        player['country'] = response['data']['player']['user']['location']['country']
        player['state'] = response['data']['player']['user']['location']['state']
        player['city'] = response['data']['player']['user']['location']['city']
    else:
        player['country'] = None
        player['state'] = None
        player['city'] = None

    player['rankings'] = response['data']['player']['rankings']

    return player

def player_show_tournaments_filter(response):
    """Filter for the get_tournaments function"""
    if response['data']['player'] is None:
        return
    if response['data']['player']['user']['tournaments']['nodes'] is None:
        return

    tournaments = []
    for node in response['data']['player']['user']['tournaments']['nodes']:
        cur_tournament = {}
        cur_tournament['name'] = node['name']
        cur_tournament['slug'] = node['slug'].split('/')[-1]
        cur_tournament['id'] = node['id']
        cur_tournament['attendees'] = node['numAttendees']
        cur_tournament['country'] = node['countryCode']
        cur_tournament['unixTimestamp'] = node['startAt']
        tournaments.append(cur_tournament)

    return tournaments

def show_players_by_sponsor_filter(response):
    """Filter for showing players by sponsor"""
    if response['data']['tournament'] is None:
        return

    if response['data']['tournament']['participants']['nodes'] is None:
        return

    players = []
    for node in response['data']['tournament']['participants']['nodes']:
        cur_player = {}
        cur_player['tag'] = node['gamerTag']
        if node['user'] is not None:
            cur_player['playerId'] = response['user']['player']['id']
            cur_player['name'] = response['user']['name']
            cur_player['country'] = response['user']['location']['country']
            cur_player['state'] = response['user']['location']['state']
            cur_player['city'] = response['user']['location']['city']
        players.append(cur_player)

    return players
