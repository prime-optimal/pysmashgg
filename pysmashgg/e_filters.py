# Event-specific filters

def event_id_filter(response, event_name):
    """Filter for the event_id function"""
    if response['data']['tournament'] is None:
        return

    for event in response['data']['tournament']['events']:
        if event['slug'].split("/")[-1] == event_name:
            return event['id']

    return

def show_events_filter(response):
    """Filter for the show_events function"""
    if response['data']['tournament'] is None:
        return

    event_list = []
    for event in response['data']['tournament']['events']:
        cur_event = {}
        cur_event['id'] = event['id']
        cur_event['name'] = event['name']
        cur_event['slug'] = event['slug'].split('/')[-1]
        cur_event['entrants'] = event['numEntrants']
        event_list.append(cur_event)

    return event_list

def show_events_brackets_filter(response, event_name):
    """Filter for the show_events_brackets function"""
    if response['data']['tournament'] is None:
        return

    brackets = {}
    for event in response['data']['tournament']['events']:
        if event['slug'].split('/')[-1] == event_name:
            bracket_ids = []
            for node in event['phaseGroups']:
                bracket_ids.append(node['id'])

            brackets['eventName'] = event['name']
            brackets['slug'] = event['slug']
            brackets['bracketIds'] = bracket_ids

    return brackets

def show_all_event_brackets_filter(response):
    """Filter for the show_all_event_brackets function"""
    if response['data']['tournament'] is None:
        return

    brackets = []
    for event in response['data']['tournament']['events']:
        cur_bracket = {}
        bracket_ids = []
        if event['phaseGroups'] is not None:
            for node in event['phaseGroups']:
                bracket_ids.append(node['id'])

        cur_bracket['eventName'] = event['name']
        cur_bracket['slug'] = event['slug']
        cur_bracket['bracketIds'] = bracket_ids
        brackets.append(cur_bracket)

    return brackets

def show_event_by_game_size_dated_filter(response, size, videogame_id):
    """Filter for the show_event_by_game_size_dated function"""
    if response['data'] is None:
        return

    if response['data']['tournaments'] is None:
        return

    if response['data']['tournaments']['nodes'] is None:
        return

    events = []
    for node in response['data']['tournaments']['nodes']:
        for event in node['events']:
            if (event['numEntrants'] is None or event['videogame']['id'] is None):
                continue
            elif event['videogame']['id'] == videogame_id and event['numEntrants'] >= size:
                cur_event = {}
                cur_event['tournamentName'] = node['name']
                cur_event['tournamentSlug'] = node['slug'].split('/')[-1]
                cur_event['tournamentId'] = node['id']
                cur_event['online'] = node['isOnline']
                cur_event['startAt'] = node['startAt']
                cur_event['endAt'] = node['endAt']
                cur_event['eventName'] = event['name']
                cur_event['eventId'] = event['id']
                cur_event['numEntrants'] = event['numEntrants']
                events.append(cur_event)

    return events

def show_sets_filter(response):
    """Filter for the show_sets function"""
    if 'data' not in response:
        return
    if response['data']['event'] is None:
        return
    if response['data']['event']['sets']['nodes'] is None:
        return

    sets = []
    for node in response['data']['event']['sets']['nodes']:
        if len(node['slots']) < 2:
            continue # This fixes a bug where player doesn't have an opponent
        if (node['slots'][0]['entrant'] is None or node['slots'][1]['entrant'] is None):
            continue # This fixes a bug when tournament ends early

        cur_set = {}
        cur_set['id'] = node['id']
        cur_set['entrant1Id'] = node['slots'][0]['entrant']['id']
        cur_set['entrant2Id'] = node['slots'][1]['entrant']['id']
        cur_set['entrant1Name'] = node['slots'][0]['entrant']['name']
        cur_set['entrant2Name'] = node['slots'][1]['entrant']['name']

        if (node['games'] is not None):
            entrant1_chars = []
            entrant2_chars = []
            game_winners_ids = []
            for game in node['games']:
                if (game['selections'] is None):
                    continue
                elif (node['slots'][0]['entrant']['id'] == game['selections'][0]['entrant']['id']):
                    entrant1_chars.append(game['selections'][0]['selectionValue'])
                    if len(game['selections']) > 1:
                        entrant2_chars.append(game['selections'][1]['selectionValue'])
                else:
                    entrant2_chars.append(game['selections'][0]['selectionValue'])
                    if len(game['selections']) > 1:
                        entrant1_chars.append(game['selections'][1]['selectionValue'])

                game_winners_ids.append(game['winnerId'])

            cur_set['entrant1Chars'] = entrant1_chars
            cur_set['entrant2Chars'] = entrant2_chars
            cur_set['gameWinners'] = game_winners_ids

        # Handle match completion and scoring
        match_done = True
        if node['slots'][0]['standing'] is None:
            cur_set['entrant1Score'] = -1
            match_done = False
        elif node['slots'][0]['standing']['stats']['score']['value'] is not None:
            cur_set['entrant1Score'] = node['slots'][0]['standing']['stats']['score']['value']
        else:
            cur_set['entrant1Score'] = -1

        if node['slots'][1]['standing'] is None:
            cur_set['entrant2Score'] = -1
            match_done = False
        elif node['slots'][1]['standing']['stats']['score']['value'] is not None:
            cur_set['entrant2Score'] = node['slots'][1]['standing']['stats']['score']['value']
        else:
            cur_set['entrant2Score'] = -1

        # Determine winner/loser
        if match_done:
            cur_set['completed'] = True
            if node['slots'][0]['standing']['placement'] == 1:
                cur_set['winnerId'] = cur_set['entrant1Id']
                cur_set['loserId'] = cur_set['entrant2Id']
                cur_set['winnerName'] = cur_set['entrant1Name']
                cur_set['loserName'] = cur_set['entrant2Name']
            elif node['slots'][0]['standing']['placement'] == 2:
                cur_set['winnerId'] = cur_set['entrant2Id']
                cur_set['loserId'] = cur_set['entrant1Id']
                cur_set['winnerName'] = cur_set['entrant2Name']
                cur_set['loserName'] = cur_set['entrant1Name']
        else:
            cur_set['completed'] = False

        cur_set['fullRoundText'] = node['fullRoundText']

        if node['phaseGroup'] is not None:
            cur_set['bracketName'] = node['phaseGroup']['phase']['name']
            cur_set['bracketId'] = node['phaseGroup']['id']
        else:
            cur_set['bracketName'] = None
            cur_set['bracketId'] = None

        # Handle player IDs for team events
        for j in range(0, 2):
            players = []
            for user in node['slots'][j]['entrant']['participants']:
                cur_player = {}
                if user['player'] is not None:
                    cur_player['playerId'] = user['player']['id']
                    cur_player['playerTag'] = user['player']['gamerTag']
                    if user['entrants'] is not None:
                        cur_player['entrantId'] = user['entrants'][0]['id']
                    else:
                        cur_player['entrantId'] = node['slots'][j]['entrant']['id']
                    players.append(cur_player)
                else:
                    cur_player['playerId'] = None
                    cur_player['playerTag'] = None
                    cur_player['entrantId'] = node['slots'][j]['entrant']['id']

            cur_set['entrant' + str(j+1) + 'Players'] = players

        sets.append(cur_set)

    return sets

def show_entrants_filter(response):
    """Filter for the show_entrants function"""
    if response['data']['event'] is None:
        return
    if response['data']['event']['standings']['nodes'] is None:
        return

    entrants = []
    for node in response['data']['event']['standings']['nodes']:
        cur_entrant = {}
        cur_entrant['entrantId'] = node['entrant']['id']
        cur_entrant['tag'] = node['entrant']['name']
        cur_entrant['finalPlacement'] = node['placement']
        if node['entrant']['seeds'] is None:
            cur_entrant['seed'] = -1
        else:
            cur_entrant['seed'] = node['entrant']['seeds'][0]['seedNum']

        players = []
        for user in node['entrant']['participants']:
            cur_player = {}
            if user['player']['id'] is not None:
                cur_player['playerId'] = user['player']['id']
            else:
                cur_player['playerId'] = "None"
            cur_player['playerTag'] = user['player']['gamerTag']
            players.append(cur_player)
        cur_entrant['entrantPlayers'] = players
        entrants.append(cur_entrant)

    return entrants

def show_lightweight_results_filter(response):
    """Filter for the show_lightweight_results function"""
    if response['data']['event'] is None:
        return
    if response['data']['event']['standings']['nodes'] is None:
        return

    entrants = []
    for node in response['data']['event']['standings']['nodes']:
        cur_entrant = {}
        cur_entrant['placement'] = node['placement']
        cur_entrant['name'] = node['entrant']['name'].split(' | ')[-1]
        cur_entrant['id'] = node['entrant']['id']

        # Add social media info
        cur_entrant['socials'] = {}
        if node['entrant']['participants']:
            for participant in node['entrant']['participants']:
                if participant.get('player') and participant['player'].get('user'):
                    if participant['player']['user'].get('authorizations'):
                        for auth in participant['player']['user']['authorizations']:
                            if auth['type'] and auth['externalUsername']:
                                cur_entrant['socials'][auth['type'].lower()] = auth['externalUsername']

        entrants.append(cur_entrant)

    return entrants
