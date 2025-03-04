from pysmashgg import filters
from pysmashgg.queries import (
    BRACKET_SHOW_ENTRANTS_QUERY,
    BRACKET_SHOW_SETS_QUERY
)
from pysmashgg.api import run_query

# Shows all the players in a bracket (aka phaseGroup)
def show_entrants(bracket_id, page_num, header, auto_retry):
    variables = {"phaseGroupId": bracket_id, "page": page_num}
    response = run_query(BRACKET_SHOW_ENTRANTS_QUERY, variables, header, auto_retry)
    data = filters.bracket_show_entrants_filter(response)
    return data

# Shows all the players in a bracket
def show_sets(bracket_id, page_num, header, auto_retry):
    variables = {"phaseGroupId": bracket_id, "page": page_num}
    response = run_query(BRACKET_SHOW_SETS_QUERY, variables, header, auto_retry)
    data = filters.bracket_show_sets_filter(response)
    return data

# THIS WAS MADE A SEPERATE FILE TO MAKE ROOM FOR FUTURE EXPANSION
