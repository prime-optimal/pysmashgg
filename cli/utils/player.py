"""Player-related utility functions."""

from typing import Optional

from .. import console
from pysmashgg.api import run_query
from pysmashgg.queries import PLAYER_LOOKUP_ID_QUERY

def format_player_slug(slug: str) -> str:
    """Format the player slug to ensure it has the correct prefix.

    Args:
        slug: The raw player slug provided by the user

    Returns:
        Properly formatted player slug with 'user/' prefix if needed
    """
    # Remove any leading/trailing whitespace
    slug = slug.strip()

    # If the slug already starts with 'user/', return it as is
    if slug.startswith('user/'):
        return slug

    # Otherwise, prepend 'user/'
    return f"user/{slug}"

def lookup_player_id(discriminator_slug: str, header: dict, auto_retry: bool) -> Optional[str]:
    """Look up a player's ID using their discriminator slug.

    Args:
        discriminator_slug: The player's discriminator slug
        header: The API request header
        auto_retry: Whether to automatically retry failed requests

    Returns:
        The player's ID if found, None otherwise
    """
    try:
        formatted_slug = format_player_slug(discriminator_slug)
        variables = {"discriminatorSlug": formatted_slug}
        response = run_query(PLAYER_LOOKUP_ID_QUERY, variables, header, auto_retry)

        if (response and 'data' in response and
            response['data'].get('user') and
            response['data']['user'].get('player') and
            response['data']['user']['player'].get('id')):
            return response['data']['user']['player']['id']

        if 'errors' in response:
            console.print("[red]API Errors:[/]")
            for error in response['errors']:
                console.print(f"[red]- {error.get('message', 'Unknown error')}[/]")

        return None
    except Exception as e:
        console.print(f"[red]Error looking up player ID:[/] {str(e)}")
        return None
