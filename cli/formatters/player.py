"""Player-related formatting functions."""

from datetime import datetime
from rich.table import Table
from rich.prompt import IntPrompt
from rich.panel import Panel
from collections import defaultdict

from .. import console
from ..formatters.player_info import create_player_info_panel
from pysmashgg.api import run_query
from pysmashgg.queries import PLAYER_RECENT_GAME_PLACEMENTS_QUERY

def display_player_info(player_data):
    """Format and display player information in a rich panel."""
    create_player_info_panel(player_data)

def display_tournament_stats(processed_standings):
    """Display tournament statistics."""
    # Count placements
    placement_counts = {
        "1st": 0,
        "2nd": 0,
        "3rd": 0
    }

    # Count tournament types
    tournament_types = {
        "Online": 0,
        "Offline": 0
    }

    total_tournaments = len(processed_standings)

    for standing in processed_standings:
        # Count placements
        if "🥇 1st" in standing['placement']:
            placement_counts["1st"] += 1
        elif "🥈 2nd" in standing['placement']:
            placement_counts["2nd"] += 1
        elif "🥉 3rd" in standing['placement']:
            placement_counts["3rd"] += 1

        # Count tournament types
        tournament_types[standing['type']] += 1

    # Calculate percentages
    online_percent = (tournament_types["Online"] / total_tournaments * 100) if total_tournaments > 0 else 0
    offline_percent = (tournament_types["Offline"] / total_tournaments * 100) if total_tournaments > 0 else 0

    # Create stats lines
    stats_lines = []

    # Add placement stats
    stats_lines.append("[bold cyan]Tournament Placements:[/]")
    stats_lines.append(f"🥇 1st Place: {placement_counts['1st']} tournament{'s' if placement_counts['1st'] != 1 else ''}")
    stats_lines.append(f"🥈 2nd Place: {placement_counts['2nd']} tournament{'s' if placement_counts['2nd'] != 1 else ''}")
    stats_lines.append(f"🥉 3rd Place: {placement_counts['3rd']} tournament{'s' if placement_counts['3rd'] != 1 else ''}")

    # Add tournament type stats
    stats_lines.append("\n[bold cyan]Tournament Types:[/]")
    stats_lines.append(f"Online: {tournament_types['Online']} ({online_percent:.1f}%)")
    stats_lines.append(f"Offline: {tournament_types['Offline']} ({offline_percent:.1f}%)")

    # Display stats in a panel
    console.print(Panel(
        "\n".join(stats_lines),
        title="Tournament Statistics",
        border_style="cyan"
    ))

def display_player_placements(placements_data, header=None, auto_retry=None):
    """Format and display player's recent placements in a table."""
    try:
        if not placements_data:
            console.print("[red]No response from API[/]")
            return

        if 'data' not in placements_data:
            console.print("[red]No data field in API response[/]")
            if 'errors' in placements_data:
                console.print("[red]API Errors:[/]")
                for error in placements_data['errors']:
                    console.print(f"[red]- {error.get('message', 'Unknown error')}[/]")
            return

        if not placements_data['data'].get('user'):
            console.print("[red]No user data in API response[/]")
            return

        if not placements_data['data']['user'].get('player'):
            console.print("[red]No player data in API response[/]")
            return

        # Display player info panel
        create_player_info_panel(placements_data)

        # Get standings data
        player = placements_data['data']['user']['player']
        standings = player.get('recentStandings', []) or []

        if not standings:
            console.print("[yellow]No recent tournament placements found[/]")
            return

        # Create placements table
        table = Table(title="Recent Tournament Placements")
        table.add_column("Date", justify="right")
        table.add_column("Tournament", style="cyan")
        table.add_column("Game", style="magenta")
        table.add_column("Placement", justify="right", style="yellow")
        table.add_column("Entrants", justify="right")
        table.add_column("Type", justify="center")

        # Track games and their counts
        game_counts = defaultdict(int)
        game_ids = {}

        # Process standings and sort by date
        processed_standings = []
        for standing in standings:
            try:
                entrant = standing.get('entrant', {}) or {}
                event = entrant.get('event', {}) or {}
                tournament = event.get('tournament', {}) or {}
                videogame = event.get('videogame', {}) or {}

                # Only process if we have the minimum required data
                if not all([standing.get('placement'), tournament.get('name')]):
                    continue

                # Track game counts and IDs
                game_name = videogame.get('displayName', 'Unknown Game')
                game_counts[game_name] += 1
                game_ids[game_name] = videogame.get('id')

                # Get timestamp from event
                timestamp = event.get('startAt', 0)

                # Format date
                date = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d') if timestamp else "N/A"

                # Format placement
                placement = standing['placement']
                if placement == 1:
                    placement = "🥇 1st"
                elif placement == 2:
                    placement = "🥈 2nd"
                elif placement == 3:
                    placement = "🥉 3rd"
                else:
                    placement = f"{placement}th"

                processed_standings.append({
                    'timestamp': timestamp,
                    'date': date,
                    'tournament': tournament.get('name', 'N/A'),
                    'game': game_name,
                    'placement': placement,
                    'entrants': str(event.get('numEntrants', 'N/A')),
                    'type': "Online" if event.get('isOnline') else "Offline"
                })

            except Exception as e:
                console.print(f"[yellow]Warning: Skipped a placement due to missing data: {str(e)}[/]")
                continue

        # Sort by date (timestamp) in descending order (most recent first)
        processed_standings.sort(key=lambda x: x['timestamp'], reverse=True)

        # Add sorted standings to table
        for standing in processed_standings:
            table.add_row(
                standing['date'],
                standing['tournament'],
                standing['game'],
                standing['placement'],
                standing['entrants'],
                standing['type']
            )

        if table.row_count > 0:
            console.print(table)

            # Display tournament statistics
            console.print()  # Add a blank line
            display_tournament_stats(processed_standings)

            # Display game counts
            console.print("\n[bold cyan]Tournaments by Game:[/]")
            game_options = {}
            option_num = 1
            for game_name, count in game_counts.items():
                game_id = game_ids.get(game_name)
                if game_id:
                    game_options[option_num] = (game_name, game_id)
                    console.print(f"{option_num}. {game_name} (ID: {game_id}): {count} tournament{'s' if count != 1 else ''}")
                    option_num += 1

            # Instead of prompting for game selection, just display the available games
            if game_options:
                console.print("\n[bold cyan]Available Games:[/]")
                for option_num, (game_name, game_id) in game_options.items():
                    console.print(f"{option_num}. {game_name} (ID: {game_id})")

                console.print("\n[yellow]To see results for a specific game, use:[/]")
                console.print("[yellow]python startgg.py results <player_slug> --game <game_id>[/]")
                console.print("[yellow]python startgg.py results <player_id> --game <game_id>[/]")
        else:
            console.print("[yellow]No valid placement data to display[/]")

    except Exception as e:
        console.print(f"[red]Error displaying player placements:[/] {str(e)}")
