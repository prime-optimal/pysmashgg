"""Tournament results command implementation."""

from datetime import datetime
from pathlib import Path
from typing import Optional
import typer
from rich.panel import Panel

from .. import app, console
from ..exporters.results_exporter import export_results
from ..formatters.results import create_results_table
from pysmashgg.tournaments import show_events
from pysmashgg.api import run_query
from pysmashgg.t_queries import SHOW_LIGHTWEIGHT_RESULTS_QUERY

# Import the global SmashGG instance
import startgg

def version_callback(value: bool):
    if value:
        from .. import __version__
        console.print(f"[cyan]SmashGG Results Fetcher v{__version__}[/]")
        raise typer.Exit()

@app.command()
def results(
    tournament_slug: str = typer.Argument(..., help="The tournament slug (e.g., 'tns-street-fighter-6-69')"),
    json_file: Optional[Path] = typer.Option(None, "--json", "-j", help="Export results to JSON file"),
    csv_file: Optional[Path] = typer.Option(None, "--csv", "-c", help="Export results to CSV file"),
    txt_file: Optional[Path] = typer.Option(None, "--txt", "-t", help="Export results to TXT file"),
    version: Optional[bool] = typer.Option(None, "--version", "-v", callback=version_callback, 
                                         help="Show the application version and exit"),
):
    """Fetch and display Top 8 results for a Smash.gg tournament."""
    try:
        # Get tournament information
        with console.status("[bold green]Fetching tournament info..."):
            tournament_info = startgg.smash.tournament_show(tournament_slug)
            
            # Display tournament info
            start_date = datetime.fromtimestamp(tournament_info['startTimestamp']).strftime('%Y-%m-%d')
            end_date = datetime.fromtimestamp(tournament_info['endTimestamp']).strftime('%Y-%m-%d')
            
            info_text = [
                f"[bold cyan]Name:[/] {tournament_info['name']}",
                f"[bold cyan]Location:[/] {tournament_info['city'] or 'N/A'}, {tournament_info['state'] or 'N/A'}",
                f"[bold cyan]Date:[/] {start_date} to {end_date}",
                f"[bold cyan]Entrants:[/] {tournament_info['entrants']}"
            ]
            
            console.print(Panel("\n".join(info_text), title="Tournament Info", border_style="cyan"))

        # Get tournament events
        with console.status("[bold green]Fetching events..."):
            events = show_events(tournament_slug, startgg.smash.header, startgg.smash.auto_retry)
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
                
                if 'data' in response and 'event' in response['data'] and 'standings' in response['data']['event']:
                    standings = response['data']['event']['standings']['nodes']
                    top_8 = []
                    for player in standings[:8]:
                        top_8.append({
                            "placement": player['placement'],
                            "name": player['entrant']['name']
                        })
                    
                    if top_8:
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
