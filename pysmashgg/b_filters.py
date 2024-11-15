# Bracket-specific filters

def bracket_show_entrants_filter(response):
    """Filter for the show_entrants function in brackets"""
    if response['data']['phaseGroup'] is None:
        return

    if response['data']['phaseGroup']['seeds']['nodes'] is None:
        return

    entrants = []
    for node in response['data']['phaseGroup']['seeds']['nodes']:
        cur_entrant = {}
        cur_entrant['entrantId'] = node['entrant']['id']
        cur_entrant['tag'] = node['entrant']['name']
        cur_entrant['finalPlacement'] = node['placement']
        cur_entrant['seed'] = node['seedNum']

        players = []
        for user in node['entrant']['participants']:
            cur_player = {}
            cur_player['playerId'] = user['player']['id']
            cur_player['playerTag'] = user['player']['gamerTag']
            players.append(cur_player)
        cur_entrant['entrantPlayers'] = players

        entrants.append(cur_entrant)

    return entrants

def bracket_show_sets_filter(response):
    """Filter for the show_sets function in brackets"""
    if response['data']['phaseGroup'] is None:
        return

    if response['data']['phaseGroup']['sets']['nodes'] is None:
        return

    bracket_name = response['data']['phaseGroup']['phase']['name']
    sets = []

    for node in response['data']['phaseGroup']['sets']['nodes']:
        cur_set = {}
        cur_set['id'] = node['id']
        cur_set['entrant1Id'] = node['slots'][0]['entrant']['id']
        cur_set['entrant2Id'] = node['slots'][1]['entrant']['id']
        cur_set['entrant1Name'] = node['slots'][0]['entrant']['name']
        cur_set['entrant2Name'] = node['slots'][1]['entrant']['name']

        # Handle match completion and scoring
        match_done = True
        if node['slots'][0]['standing'] is None:
            cur_set['entrant1Score'] = -1
            match_done = False
        elif node['slots'][0]['standing']['stats']['score']['value'] is not None:
            cur_set['entrant1Score'] = node['slots'][0]['standing']['stats']['score']['value']
        else:
            cur_set['entrant1Score'] = -1

        if node['slots'][0]['standing'] is None:
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

        cur_set['bracketName'] = bracket_name

        # Handle player information
        for j in range(0, 2):
            players = []
            for user in node['slots'][j]['entrant']['participants']:
                cur_player = {}
                cur_player['playerId'] = user['player']['id']
                cur_player['playerTag'] = user['player']['gamerTag']
                players.append(cur_player)

            cur_set['entrant' + str(j+1) + 'Players'] = players

        sets.append(cur_set)

    return sets

def show_head_to_head_filter(response, player2_name):
    """Filter for the show_head_to_head function"""
    if response['data']['event'] is None:
        return

    if response['data']['event']['sets']['nodes'] is None:
        return

    sets = []
    for node in response['data']['event']['sets']['nodes']:
        # Check if player2 is in this set
        if ((node['slots'][0]['entrant']['name'].split('|')[-1]).lower() == player2_name.lower()
            or node['slots'][0]['entrant']['name'].lower() == player2_name.lower()
            or (node['slots'][1]['entrant']['name'].split('|')[-1]).lower() == player2_name.lower()
            or node['slots'][1]['entrant']['name'].lower() == player2_name.lower()):

            cur_set = {}
            cur_set['id'] = node['id']
            cur_set['entrant1Id'] = node['slots'][0]['entrant']['id']
            cur_set['entrant2Id'] = node['slots'][1]['entrant']['id']
            cur_set['entrant1Name'] = node['slots'][0]['entrant']['name']
            cur_set['entrant2Name'] = node['slots'][1]['entrant']['name']

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

            cur_set['setRound'] = node['fullRoundText']
            cur_set['bracketId'] = node['phaseGroup']['id']

            sets.append(cur_set)

    return sets
