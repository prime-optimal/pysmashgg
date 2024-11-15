# Tournament-specific filters

def show_filter(response):
    """Filter for the show function"""
    if response['data']['tournament'] is None:
        return

    data = {}
    data['id'] = response['data']['tournament']['id']
    data['name'] = response['data']['tournament']['name']
    data['country'] = response['data']['tournament']['countryCode']
    data['state'] = response['data']['tournament']['addrState']
    data['city'] = response['data']['tournament']['city']
    data['startTimestamp'] = response['data']['tournament']['startAt']
    data['endTimestamp'] = response['data']['tournament']['endAt']
    data['entrants'] = response['data']['tournament']['numAttendees']

    return data

def show_with_brackets_filter(response, event_name):
    """Filter for the show_with_brackets function"""
    if response['data']['tournament'] is None:
        return

    data = {}
    data['id'] = response['data']['tournament']['id']
    data['name'] = response['data']['tournament']['name']
    data['country'] = response['data']['tournament']['countryCode']
    data['state'] = response['data']['tournament']['addrState']
    data['city'] = response['data']['tournament']['city']
    data['startTimestamp'] = response['data']['tournament']['startAt']
    data['endTimestamp'] = response['data']['tournament']['endAt']
    data['entrants'] = response['data']['tournament']['numAttendees']

    for event in response['data']['tournament']['events']:
        if event['slug'].split("/")[-1] == event_name:
            data['eventId'] = event['id']
            data['eventName'] = event['name']
            data['eventSlug'] = event['slug'].split('/')[-1]
            bracket_ids = []
            if event['phaseGroups'] is not None:
                for node in event['phaseGroups']:
                    bracket_ids.append(node['id'])
            data['bracketIds'] = bracket_ids
            break

    return data

def show_with_brackets_all_filter(response):
    """Filter for the show_with_brackets_all function"""
    if response['data']['tournament'] is None:
        return

    data = {}
    data['id'] = response['data']['tournament']['id']
    data['name'] = response['data']['tournament']['name']
    data['country'] = response['data']['tournament']['countryCode']
    data['state'] = response['data']['tournament']['addrState']
    data['city'] = response['data']['tournament']['city']
    data['startTimestamp'] = response['data']['tournament']['startAt']
    data['endTimestamp'] = response['data']['tournament']['endAt']
    data['entrants'] = response['data']['tournament']['numAttendees']

    for event in response['data']['tournament']['events']:
        bracket_ids = []
        if event['phaseGroups'] is not None:
            for node in event['phaseGroups']:
                bracket_ids.append(node['id'])

        del event['phaseGroups']
        event['bracketIds'] = bracket_ids

    data['events'] = response['data']['tournament']['events']

    return data

def show_by_country_filter(response):
    """Filter for the show_by_country function"""
    if response['data']['tournaments'] is None:
        return

    if response['data']['tournaments']['nodes'] is None:
        return

    tournaments = []
    for node in response['data']['tournaments']['nodes']:
        cur_tournament = {}
        cur_tournament['id'] = node['id']
        cur_tournament['name'] = node['name']
        cur_tournament['slug'] = node['slug'].split('/')[-1]
        cur_tournament['entrants'] = node['numAttendees']
        cur_tournament['state'] = node['addrState']
        cur_tournament['city'] = node['city']
        cur_tournament['startTimestamp'] = node['startAt']
        cur_tournament['endTimestamp'] = node['endAt']
        tournaments.append(cur_tournament)

    return tournaments

def show_by_state_filter(response):
    """Filter for the show_by_state function"""
    if response['data']['tournaments'] is None:
        return

    if response['data']['tournaments']['nodes'] is None:
        return

    tournaments = []
    for node in response['data']['tournaments']['nodes']:
        cur_tournament = {}
        cur_tournament['id'] = node['id']
        cur_tournament['name'] = node['name']
        cur_tournament['slug'] = node['slug'].split('/')[-1]
        cur_tournament['entrants'] = node['numAttendees']
        cur_tournament['city'] = node['city']
        cur_tournament['startTimestamp'] = node['startAt']
        cur_tournament['endTimestamp'] = node['endAt']
        tournaments.append(cur_tournament)

    return tournaments

def show_by_radius_filter(response):
    """Filter for the show_by_radius function"""
    if response['data']['tournaments'] is None:
        return

    if response['data']['tournaments']['nodes'] is None:
        return

    tournaments = []
    for node in response['data']['tournaments']['nodes']:
        cur_tournament = {}
        cur_tournament['id'] = node['id']
        cur_tournament['name'] = node['name']
        cur_tournament['slug'] = node['slug'].split('/')[-1]
        cur_tournament['entrants'] = node['numAttendees']
        cur_tournament['country'] = node['countryCode']
        cur_tournament['state'] = node['addrState']
        cur_tournament['city'] = node['city']
        cur_tournament['startTimestamp'] = node['startAt']
        cur_tournament['endTimestamp'] = node['endAt']
        tournaments.append(cur_tournament)

    return tournaments

def show_by_owner_filter(response):
    """Filter for the show_by_owner function"""
    if response['data']['tournaments'] is None:
        return

    if response['data']['tournaments']['nodes'] is None:
        return

    tournaments = []
    for node in response['data']['tournaments']['nodes']:
        cur_tournament = {}
        cur_tournament['id'] = node['id']
        cur_tournament['name'] = node['name']
        cur_tournament['slug'] = node['slug'].split('/')[-1]
        cur_tournament['entrants'] = node['numAttendees']
        cur_tournament['country'] = node['countryCode']
        cur_tournament['state'] = node['addrState']
        cur_tournament['city'] = node['city']
        cur_tournament['startTimestamp'] = node['startAt']
        cur_tournament['endTimestamp'] = node['endAt']
        tournaments.append(cur_tournament)

    return tournaments
