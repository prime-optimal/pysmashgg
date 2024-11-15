"""Tournament results command implementation."""

from datetime import datetime
from pathlib import Path
from typing import Optional
import typer
from rich.panel import Panel
import time

from .. import app, console
from ..exporters.results_exporter import export_results
from ..formatters.results import create_results_table
from pysmashgg.tournaments import show_events
from pysmashgg.api import run_query
from pysmashgg.queries import (
    SHOW_LIGHTWEIGHT_RESULTS_QUERY,
    SHOW_EVENTS_QUERY
)
from pysmashgg import filters

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
    """Fetch and display tournament results.

    Examples:
    1. Get tournament results:
        python startgg.py results tournament-slug

    2. Export results to a file:
        python startgg.py results tournament-slug --json results.json
    """
    try:
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

            try:
                with console.status(f"[bold green]Fetching results for {event_name}..."):
                    # Add a small delay between API calls to avoid rate limiting
                    time.sleep(0.5)

                    variables = {"eventId": event_id, "page": 1}
                    response = run_query(SHOW_LIGHTWEIGHT_RESULTS_QUERY, variables, startgg.smash.header, startgg.smash.auto_retry)

                    # Check for API errors
                    if not response:
                        console.print(f"[yellow]Could not fetch results for {event_name} - API returned no data[/]")
                        continue

                    if 'errors' in response:
                        error_messages = [error.get('message', 'Unknown error') for error in response['errors']]
                        console.print(f"[yellow]API Errors for {event_name}:[/]")
                        for msg in error_messages:
                            console.print(f"[yellow]- {msg}[/]")
                        continue

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

            except Exception as e:
                console.print(f"[yellow]Error processing {event_name}: {str(e)}[/]")
                # Continue with next event instead of stopping
                continue

        # Export results if requested
        if any([json_file, csv_file, txt_file]) and all_results:
            export_results(all_results, json_file, csv_file, txt_file)

    except Exception as e:
        console.print(f"[red]Error:[/] {str(e)}")
        raise typer.Exit(code=1)
