# League-specific filters

def league_show_filter(response):
    """Filter for showing league information"""
    if response['data']['league'] is None:
        return

    league = {}
    league_data = response['data']['league']
    league['id'] = league_data['id']
    league['name'] = league_data['name']
    league['startAt'] = league_data.get('startAt')
    league['endAt'] = league_data.get('endAt')
    if 'slug' in league_data:
        league['slug'] = league_data['slug']

    return league
