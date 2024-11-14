"""Tournament and player results command implementation."""

from datetime import datetime
from pathlib import Path
from typing import Optional
import typer
from rich.panel import Panel
from rich.table import Table

from .. import app, console
from ..exporters.results_exporter import export_results
from ..formatters.results import create_results_table
from ..formatters.sets import create_sets_table
from pysmashgg.tournaments import show_events
from pysmashgg.api import run_query
from pysmashgg.t_queries import SHOW_LIGHTWEIGHT_RESULTS_QUERY
from pysmashgg.p_queries import (
    PLAYER_RECENT_PLACEMENTS_QUERY, 
    PLAYER_LOOKUP_ID_QUERY,
    PLAYER_SETS_QUERY
)
from pysmashgg import filters

# Import the global SmashGG instance
import startgg

def version_callback(value: bool):
    if value:
        from .. import __version__
        console.print(f"[cyan]SmashGG Results Fetcher v{__version__}[/]")
        raise typer.Exit()

def format_player_slug(slug: str) -> str:
    """Format the player slug to ensure it has the correct prefix."""
    slug = slug.strip()
    return slug if slug.startswith('user/') else f"user/{slug}"

def lookup_player_id(discriminator_slug: str) -> Optional[str]:
    """Look up a player's ID using their discriminator slug.
    
    Args:
        discriminator_slug: The player's discriminator slug
        
    Returns:
        The player's ID if found, None otherwise
    """
    try:
        formatted_slug = format_player_slug(discriminator_slug)
        variables = {"discriminatorSlug": formatted_slug}
        response = run_query(PLAYER_LOOKUP_ID_QUERY, variables, startgg.smash.header, startgg.smash.auto_retry)
        
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

        player = placements_data['data']['player']
        standings = player.get('recentStandings', []) or []

        # Create player info panel
        player_info = []
        
        # Add player info only if available
        if player.get('gamerTag'):
            player_info.append(f"[bold cyan]Player:[/] {player['gamerTag']}")
        if player.get('prefix'):
            player_info.append(f"[bold cyan]Prefix:[/] {player['prefix']}")
        if player.get('id'):
            player_info.append(f"[bold cyan]ID:[/] {player['id']}")

        if player.get('user'):
            user = player['user']
            if user.get('location'):
                loc = user['location']
                location_parts = []
                if loc.get('city'): location_parts.append(loc['city'])
                if loc.get('state'): location_parts.append(loc['state'])
                if loc.get('country'): location_parts.append(loc['country'])
                if location_parts:
                    player_info.append(f"[bold cyan]Location:[/] {', '.join(location_parts)}")

        if not player_info:
            player_info.append("[yellow]No player information available[/]")

        console.print(Panel("\n".join(player_info), title="Player Information", border_style="cyan"))

        if not standings:
            console.print("[yellow]No recent tournament placements found[/]")
            return

        # Create placements table
        table = Table(title="Recent Tournament Placements")
        table.add_column("Tournament", style="cyan")
        table.add_column("Event", style="green")
        table.add_column("Placement", justify="right", style="yellow")
        table.add_column("Entrants", justify="right")
        table.add_column("Date", justify="right")
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

                # Get timestamp for sorting
                timestamp = tournament.get('startAt', 0)
                
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
                    'tournament': tournament.get('name', 'N/A'),
                    'event': event.get('name', 'N/A'),
                    'placement': placement,
                    'entrants': str(event.get('numEntrants', 'N/A')),
                    'date': date,
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
                standing['tournament'],
                standing['event'],
                standing['placement'],
                standing['entrants'],
                standing['date'],
                standing['type']
            )

        if table.row_count > 0:
            console.print(table)
        else:
            console.print("[yellow]No valid placement data to display[/]")

    except Exception as e:
        console.print(f"[red]Error displaying player placements:[/] {str(e)}")

@app.command()
def results(
    tournament_slug: Optional[str] = typer.Argument(None, help="The tournament slug (e.g., 'tns-street-fighter-6-69')"),
    player_slug: Optional[str] = typer.Option(None, "--player", "-p", help="Get recent placements for a player (use their profile slug/ID from start.gg URL)"),
    game_id: Optional[str] = typer.Option(None, "--game", "-g", help="Game ID for player placements (required with --player)"),
    sets: bool = typer.Option(False, "--sets", "-s", help="Show player's sets for their recent events"),
    json_file: Optional[Path] = typer.Option(None, "--json", "-j", help="Export results to JSON file"),
    csv_file: Optional[Path] = typer.Option(None, "--csv", "-c", help="Export results to CSV file"),
    txt_file: Optional[Path] = typer.Option(None, "--txt", "-t", help="Export results to TXT file"),
    version: Optional[bool] = typer.Option(None, "--version", "-v", callback=version_callback, 
                                         help="Show the application version and exit"),
):
    """Fetch and display tournament results or player placements.
    
    This command can be used in several ways:
    1. View tournament results by providing a tournament slug
    2. View a player's recent placements by providing their profile slug/ID and game ID
    3. View a player's recent sets by adding the --sets flag
    
    Examples:
    1. Get tournament results:
        python startgg.py results tournament-slug
        
    2. Get player placements:
        python startgg.py results --player "06989544" --game "43868"
        
    3. Get player sets:
        python startgg.py results --player "06989544" --game "43868" --sets
        
    Note: For player data, use the ID from their start.gg profile URL.
    For example, if their profile is at start.gg/user/06989544, use "06989544".
    """
    try:
        # Handle player placements and sets
        if player_slug:
            if not game_id:
                console.print("[red]Error: --game option is required when viewing player data[/]")
                return
                
            # First lookup the player's ID using their discriminator slug
            with console.status(f"[bold green]Looking up player ID for {player_slug}..."):
                player_id = lookup_player_id(player_slug)
                if not player_id:
                    console.print("[red]Could not find player ID. Make sure the profile slug/ID is correct.[/]")
                    return
                
                console.print(f"[green]Found player ID: {player_id}[/]")
                
            # Validate game_id as numeric
            try:
                game_id_int = int(game_id)
            except ValueError:
                console.print("[red]Error: Game ID must be a numeric value[/]")
                return
                
            # Fetch placements
            with console.status(f"[bold green]Fetching placements..."):
                variables = {"playerId": player_id, "videogameId": str(game_id_int)}
                response = run_query(PLAYER_RECENT_PLACEMENTS_QUERY, variables, startgg.smash.header, startgg.smash.auto_retry)
                display_player_placements(response)

            # If sets flag is set, fetch and display sets
            if sets:
                # Get the most recent event ID from placements
                if (response and 'data' in response and 
                    response['data'].get('player') and 
                    response['data']['player'].get('recentStandings')):
                    
                    standings = response['data']['player']['recentStandings']
                    if standings:
                        recent_event = standings[0]['entrant']['event']
                        event_id = recent_event['id']
                        is_online = recent_event['isOnline']
                        
                        with console.status(f"[bold green]Fetching sets for most recent event..."):
                            variables = {
                                "playerId": player_id,
                                "isOnline": is_online,
                                "eventId": [event_id]
                            }
                            sets_response = run_query(PLAYER_SETS_QUERY, variables, startgg.smash.header, startgg.smash.auto_retry)
                            create_sets_table(sets_response)
            return

        # Handle tournament results
        if not tournament_slug:
            console.print("[red]Error: Tournament slug is required when not using --player option[/]")
            return

        # Get tournament information
        with console.status("[bold green]Fetching tournament info..."):
            tournament_info = startgg.smash.tournament_show(tournament_slug)
            if not tournament_info:
                console.print("[red]Could not find tournament information[/]")
                return
            
            # Display tournament info
            start_date = datetime.fromtimestamp(tournament_info['startTimestamp']).strftime('%Y-%m-%d')
            end_date = datetime.fromtimestamp(tournament_info['endTimestamp']).strftime('%Y-%m-%d')
            
            # Format location, showing "Online" if no city/state available
            city = tournament_info.get('city')
            state = tournament_info.get('state')
            location = f"{city}, {state}" if city and state else "Online"
            
            info_text = [
                f"[bold cyan]Name:[/] {tournament_info['name']}",
                f"[bold cyan]URL:[/] https://start.gg/tournament/{tournament_slug}",
                f"[bold cyan]Location:[/] {location}",
                f"[bold cyan]Date:[/] {start_date} to {end_date}",
                f"[bold cyan]Entrants:[/] {tournament_info['entrants']}"
            ]

            # Add tournament organizer info if available
            if 'owner' in tournament_info and tournament_info['owner']:
                info_text.append(f"[bold cyan]Tournament Organizer:[/] {tournament_info['owner']['name']} (ID: {tournament_info['owner']['id']})")
            
            console.print(Panel("\n".join(info_text), title="Tournament Info", border_style="cyan"))

        # Get tournament events
        with console.status("[bold green]Fetching events..."):
            events = show_events(tournament_slug, startgg.smash.header, startgg.smash.auto_retry)
            if not events:
                console.print("[red]Could not find any events for this tournament[/]")
                return
                
            console.print(f"\nFound [cyan]{len(events)}[/] events for tournament: [bold]{tournament_info['name']}[/]")

        # Store all results for potential export
        all_results = {}

        # Fetch and display Top 8 for each event
        for event in events:
            event_name = event['name']
            event_id = event['id']
            
            with console.status(f"[bold green]Fetching results for {event_name}..."):
                variables = {"eventId": event_id, "page": 1}
                response = run_query(SHOW_LIGHTWEIGHT_RESULTS_QUERY, variables, startgg.smash.header, startgg.smash.auto_retry)
                standings = filters.show_lightweight_results_filter(response)
                
                if standings:
                    top_8 = standings[:8]
                    all_results[event_name] = top_8
                    total_players = len(standings)
                    
                    # Display results in a table
                    table = create_results_table(event_name, top_8, total_players)
                    console.print(table)
                else:
                    console.print(f"[yellow]No results found for {event_name}[/]")

        # Export results if requested
        if any([json_file, csv_file, txt_file]):
            export_results(all_results, json_file, csv_file, txt_file)

    except Exception as e:
        console.print(f"[red]Error:[/] {str(e)}")
        raise typer.Exit(code=1)
