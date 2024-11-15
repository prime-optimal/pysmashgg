"""Player-related formatting functions."""

from datetime import datetime
from rich.table import Table

from .. import console
from .player_info import create_player_info_panel

def display_player_info(player_data):
    """Format and display player information in a rich panel."""
    create_player_info_panel(player_data)

def display_player_placements(placements_data):
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

        if not placements_data['data'].get('player'):
            console.print("[red]No player data in API response[/]")
            return

        # Display player info panel
        create_player_info_panel(placements_data)

        # Get standings data
        player = placements_data['data']['player']
        standings = player.get('recentStandings', []) or []

        if not standings:
            console.print("[yellow]No recent tournament placements found[/]")
            return

        # Create placements table
        table = Table(title="Recent Tournament Placements")
        table.add_column("Date", justify="right")
        table.add_column("Tournament", style="cyan")
        table.add_column("Event", style="green")
        table.add_column("Placement", justify="right", style="yellow")
        table.add_column("Entrants", justify="right")
        table.add_column("Type", justify="center")

        # Process standings and sort by date
        processed_standings = []
        for standing in standings:
            try:
                entrant = standing.get('entrant', {}) or {}
                event = entrant.get('event', {}) or {}
                tournament = event.get('tournament', {}) or {}

                # Only process if we have the minimum required data
                if not all([standing.get('placement'), event.get('name'), tournament.get('name')]):
                    continue

                # Get timestamp from event instead of tournament for accurate date
                timestamp = event.get('startAt', tournament.get('startAt', 0))

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
                    'event': event.get('name', 'N/A'),
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
                standing['event'],
                standing['placement'],
                standing['entrants'],
                standing['type']
            )

        if table.row_count > 0:
            console.print(table)
        else:
            console.print("[yellow]No valid placement data to display[/]")

    except Exception as e:
        console.print(f"[red]Error displaying player placements:[/] {str(e)}")
