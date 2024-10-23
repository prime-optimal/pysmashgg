#!/usr/bin/env python3

import os
import json
import csv
from datetime import datetime
from typing import Optional
from pathlib import Path

import typer
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt
from dotenv import load_dotenv
import pysmashgg
from pysmashgg.tournaments import show_events
from pysmashgg.api import run_query
from pysmashgg.t_queries import SHOW_LIGHTWEIGHT_RESULTS_QUERY

# Initialize Typer app and Rich console
app = typer.Typer(help="Fetch and display Smash.gg tournament information")
console = Console()

# Load environment variables and initialize SmashGG
load_dotenv()
smash = pysmashgg.SmashGG(os.getenv('KEY'))

def version_callback(value: bool):
    if value:
        console.print("[cyan]SmashGG Results Fetcher v1.4.0[/]")
        raise typer.Exit()

@app.callback()
def callback():
    """
    Fetch and display Smash.gg tournament information
    """
    pass

@app.command()
def search(
    owner_id: int = typer.Argument(..., help="The tournament organizer's ID"),
    page: int = typer.Option(1, "--page", "-p", help="Page number for results"),
    limit: int = typer.Option(10, "--limit", "-l", help="Number of tournaments to display"),
    select: bool = typer.Option(False, "--select", "-s", help="Interactively select a tournament to view results")
):
    """
    Search for tournaments by owner ID
    """
    try:
        with console.status("[bold green]Searching for tournaments..."):
            tournaments = smash.tournament_show_by_owner(owner_id, page)

        if not tournaments:
            console.print("[yellow]No tournaments found for this owner ID[/]")
            return

        # Create a table to display the tournaments
        table = Table(title=f"Tournaments by Owner ID: {owner_id}")
        table.add_column("#", style="cyan", justify="right")
        table.add_column("Name", style="green")
        table.add_column("Date", style="yellow")
        table.add_column("Location", style="blue")
        table.add_column("Entrants", justify="right", style="magenta")
        table.add_column("Slug", style="white", overflow="fold")

        # Add tournaments to the table
        displayed_tournaments = []
        for idx, tournament in enumerate(tournaments[:limit], 1):
            start_date = datetime.fromtimestamp(tournament.get('startAt', 0)).strftime('%Y-%m-%d')
            location = f"{tournament.get('city', 'N/A')}, {tournament.get('state', 'N/A')}"
            entrants = str(tournament.get('numAttendees', 'N/A'))
            
            table.add_row(
                str(idx),
                tournament['name'],
                start_date,
                location,
                entrants,
                tournament['slug']
            )
            displayed_tournaments.append(tournament)

        console.print(table)
        
        if len(tournaments) > limit:
            console.print(f"\n[yellow]Showing {limit} of {len(tournaments)} tournaments. Use --limit to see more.[/]")

        if select:
            # Allow user to select a tournament and view its results
            choice = Prompt.ask(
                "\nEnter tournament number to view results",
                choices=[str(i) for i in range(1, len(displayed_tournaments) + 1)],
                show_choices=False
            )
            
            selected_tournament = displayed_tournaments[int(choice) - 1]
            console.print(f"\n[green]Selected tournament:[/] {selected_tournament['name']}")
            
            # Call the results command for the selected tournament
            results(selected_tournament['slug'])
        else:
            # Add a tip about using the tournament slug
            console.print("\n[cyan]Tips:[/]")
            console.print("1. Use the tournament slug with the 'results' command to view tournament results:")
            console.print("[green]   python startgg.py results <tournament-slug>[/]")
            console.print("2. Use --select (-s) flag to interactively select a tournament:")
            console.print("[green]   python startgg.py search <owner-id> --select[/]")

    except Exception as e:
        console.print(f"[red]Error:[/] {str(e)}")
        raise typer.Exit(code=1)

@app.command()
def results(
    tournament_slug: str = typer.Argument(..., help="The tournament slug (e.g., 'tns-street-fighter-6-69')"),
    json_file: Optional[Path] = typer.Option(None, "--json", "-j", help="Export results to JSON file"),
    csv_file: Optional[Path] = typer.Option(None, "--csv", "-c", help="Export results to CSV file"),
    txt_file: Optional[Path] = typer.Option(None, "--txt", "-t", help="Export results to TXT file"),
    version: Optional[bool] = typer.Option(None, "--version", "-v", callback=version_callback, 
                                         help="Show the application version and exit"),
):
    """
    Fetch and display Top 8 results for a Smash.gg tournament
    """
    try:
        # Get tournament information
        with console.status("[bold green]Fetching tournament info..."):
            tournament_info = smash.tournament_show(tournament_slug)
            
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
            events = show_events(tournament_slug, smash.header, smash.auto_retry)
            console.print(f"\nFound [cyan]{len(events)}[/] events for tournament: [bold]{tournament_info['name']}[/]")

        # Store all results for potential export
        all_results = {}

        # Fetch and display Top 8 for each event
        for event in events:
            event_name = event['name']
            event_id = event['id']
            
            with console.status(f"[bold green]Fetching results for {event_name}..."):
                variables = {"eventId": event_id, "page": 1}
                response = run_query(SHOW_LIGHTWEIGHT_RESULTS_QUERY, variables, smash.header, smash.auto_retry)
                
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
                        table = Table(title=f"{event_name} Top 8 ({total_players} players total)")
                        table.add_column("Place", justify="right", style="cyan")
                        table.add_column("Player", style="white")
                        
                        for player in top_8:
                            table.add_row(str(player['placement']), player['name'])
                        
                        console.print(table)
                    else:
                        console.print(f"[yellow]No results found for {event_name}[/]")

        # Export results if requested
        if json_file:
            with open(json_file, 'w') as f:
                json.dump(all_results, f, indent=2)
            console.print(f"\n[green]Results exported to {json_file} in JSON format.[/]")
            
        if csv_file:
            with open(csv_file, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(["Event", "Placement", "Name"])
                for event in all_results:
                    for player in all_results[event]:
                        writer.writerow([event, player["placement"], player["name"]])
            console.print(f"[green]Results exported to {csv_file} in CSV format.[/]")
            
        if txt_file:
            with open(txt_file, 'w') as f:
                for event in all_results:
                    f.write(f"{event}:\n")
                    for player in all_results[event]:
                        f.write(f"{player['placement']}: {player['name']}\n")
                    f.write("\n")
            console.print(f"[green]Results exported to {txt_file} in TXT format.[/]")

    except Exception as e:
        console.print(f"[red]Error:[/] {str(e)}")
        raise typer.Exit(code=1)

if __name__ == "__main__":
    app()
