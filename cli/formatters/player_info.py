"""Player information panel formatter."""

from datetime import datetime
from rich.panel import Panel
from .. import console

def create_player_info_panel(player_data):
    """Create a panel displaying comprehensive player information.

    Args:
        player_data: Player data from the API response

    Returns:
        None - Prints the panel directly
    """
    try:
        if not player_data or 'data' not in player_data:
            console.print("[red]No player data found[/]")
            return

        # Handle different query response formats
        data = player_data['data']
        if 'user' in data:
            # Handle PLAYER_BY_SLUG_QUERY and new PLAYER_RECENT_PLACEMENTS_QUERY response format
            user = data['user']
            player = user.get('player', {}) or {}
            # For the new PLAYER_RECENT_PLACEMENTS_QUERY, also check player.user for additional info
            player_user = player.get('user', {})
            # Merge authorizations from both user and player.user if they exist
            user_auth = user.get('authorizations', [])
            player_user_auth = player_user.get('authorizations', []) if player_user else []
            all_auth = user_auth + [auth for auth in player_user_auth if auth not in user_auth]
        else:
            # Handle PLAYER_INFO_QUERY response format
            player = data.get('player', {})
            if not player:
                console.print("[red]No player data found[/]")
                return
            user = player.get('user', {})
            all_auth = user.get('authorizations', [])

        info_lines = []

        # Basic player info
        if player.get('prefix'):
            info_lines.append(f"[bold cyan]Team:[/] {player['prefix']}")
        if player.get('gamerTag'):
            info_lines.append(f"[bold cyan]Tag:[/] {player['gamerTag']}")

        # User info
        if user:
            if user.get('name'):
                info_lines.append(f"[bold cyan]Name:[/] {user['name']}")
            elif player_user and player_user.get('name'):  # Fallback to player.user.name
                info_lines.append(f"[bold cyan]Name:[/] {player_user['name']}")

            if user.get('slug'):
                info_lines.append(f"[bold cyan]Profile:[/] https://start.gg/{user['slug']}")
            elif user.get('discriminator'):  # Fallback to discriminator if slug not available
                info_lines.append(f"[bold cyan]Profile:[/] start.gg/user/{user['discriminator']}")

            # Location
            location = user.get('location', {})
            if location:
                loc_parts = []
                if location.get('city'): loc_parts.append(location['city'])
                if location.get('state'): loc_parts.append(location['state'])
                if location.get('country'): loc_parts.append(location['country'])
                if loc_parts:
                    info_lines.append(f"[bold cyan]Location:[/] {', '.join(loc_parts)}")

            # Social media - now using merged authorizations
            if all_auth:
                info_lines.append("\n[bold cyan]Social Media:[/]")
                for social in all_auth:
                    if social.get('type') and social.get('externalUsername'):
                        platform = social['type'].title()
                        username = social['externalUsername']
                        url = social.get('url', '')
                        info_lines.append(f"• {platform}: {username}")
                        if url:
                            info_lines.append(f"  {url}")

            # Recent events (only in PLAYER_BY_SLUG_QUERY response)
            events = user.get('events', {})
            if events and events.get('nodes'):
                nodes = events['nodes']
                if nodes:
                    info_lines.append("\n[bold cyan]Recent Events:[/]")
                    for event in nodes[:5]:  # Show only the 5 most recent events
                        if event.get('startAt') and event.get('name') and event.get('numEntrants'):
                            date = datetime.fromtimestamp(event['startAt']).strftime('%Y-%m-%d')
                            game_name = event.get('videogame', {}).get('name', '')
                            event_info = f"• {event['name']} ({date}) - {event['numEntrants']} entrants"
                            if game_name:
                                event_info += f" - {game_name}"
                            info_lines.append(event_info)

        if not info_lines:
            info_lines.append("[yellow]No player information available[/]")

        console.print(Panel(
            "\n".join(info_lines),
            title="Player Information",
            border_style="cyan"
        ))

    except Exception as e:
        console.print(f"[red]Error displaying player information:[/] {str(e)}")
