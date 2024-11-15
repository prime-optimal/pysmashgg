# Import all filters from their respective modules
from pysmashgg.t_filters import (
    show_filter,
    show_with_brackets_filter,
    show_with_brackets_all_filter,
    show_by_country_filter,
    show_by_state_filter,
    show_by_radius_filter,
    show_by_owner_filter
)

from pysmashgg.p_filters import (
    player_id_filter,
    player_show_info_filter,
    player_show_tournaments_filter,
    show_players_by_sponsor_filter
)

from pysmashgg.e_filters import (
    event_id_filter,
    show_events_filter,
    show_events_brackets_filter,
    show_all_event_brackets_filter,
    show_event_by_game_size_dated_filter,
    show_sets_filter,
    show_entrants_filter,
    show_lightweight_results_filter
)

from pysmashgg.b_filters import (
    bracket_show_entrants_filter,
    bracket_show_sets_filter,
    show_head_to_head_filter
)

from pysmashgg.l_filters import (
    league_show_filter
)

# Export all filters
__all__ = [
    # Tournament filters
    'show_filter',
    'show_with_brackets_filter',
    'show_with_brackets_all_filter',
    'show_by_country_filter',
    'show_by_state_filter',
    'show_by_radius_filter',
    'show_by_owner_filter',

    # Player filters
    'player_id_filter',
    'player_show_info_filter',
    'player_show_tournaments_filter',
    'show_players_by_sponsor_filter',

    # Event filters
    'event_id_filter',
    'show_events_filter',
    'show_events_brackets_filter',
    'show_all_event_brackets_filter',
    'show_event_by_game_size_dated_filter',
    'show_sets_filter',
    'show_entrants_filter',
    'show_lightweight_results_filter',

    # Bracket filters
    'bracket_show_entrants_filter',
    'bracket_show_sets_filter',
    'show_head_to_head_filter',

    # League filters
    'league_show_filter'
]
