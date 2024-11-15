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

        # Handle both direct player data and user->player data structures
        if 'user' in player_data['data']:
            # Handle PLAYER_BY_SLUG_QUERY response format
            user = player_data['data']['user']
            player = user.get('player', {}) or {}
        else:
            # Handle PLAYER_INFO_QUERY and PLAYER_RECENT_PLACEMENTS_QUERY response format
            player = player_data['data'].get('player', {})
            if not player:
                console.print("[red]No player data found[/]")
                return
            user = player.get('user', {})

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

            # Social media
            socials = user.get('authorizations', [])
            if socials:
                info_lines.append("\n[bold cyan]Social Media:[/]")
                for social in socials:
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
                            info_lines.append(f"• {event['name']} ({date}) - {event['numEntrants']} entrants")

        if not info_lines:
            info_lines.append("[yellow]No player information available[/]")

        console.print(Panel(
            "\n".join(info_lines),
            title="Player Information",
            border_style="cyan"
        ))

    except Exception as e:
        console.print(f"[red]Error displaying player information:[/] {str(e)}")
