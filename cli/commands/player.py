"""Player-related command implementation."""

import typer

from .. import app, console
from ..formatters.player import display_player_info, display_player_placements
from ..formatters.player_info import create_player_info_panel
from ..formatters.sets import create_sets_table
from ..utils.player import format_player_slug, lookup_player_id
from pysmashgg.api import run_query
from pysmashgg.queries import (
    PLAYER_INFO_QUERY,
    PLAYER_RECENT_PLACEMENTS_QUERY,
    PLAYER_SETS_QUERY
)

# Import the global SmashGG instance
import startgg

player_app = typer.Typer(help="Player-related commands")
app.add_typer(player_app, name="player")

@player_app.command(name="info")
def player_info(
    player_slug: str = typer.Argument(..., help="The player's profile slug/ID from their start.gg URL")
):
    """Show detailed information about a player."""
    try:
        # First lookup the player's ID using their discriminator slug
        with console.status(f"[bold green]Looking up player ID for {player_slug}..."):
            player_id = lookup_player_id(player_slug, startgg.smash.header, startgg.smash.auto_retry)
            if not player_id:
                console.print("[red]Could not find player ID. Make sure the profile slug/ID is correct.[/]")
                return

            console.print(f"[green]Found player ID: {player_id}[/]")

        # Fetch player info
        with console.status(f"[bold green]Fetching player information..."):
            variables = {"playerId": player_id}
            response = run_query(PLAYER_INFO_QUERY, variables, startgg.smash.header, startgg.smash.auto_retry)
            create_player_info_panel(response)
    except Exception as e:
        console.print(f"[red]Error:[/] {str(e)}")
        raise typer.Exit(code=1)

@player_app.command(name="results")
def player_results(
    player_slug: str = typer.Argument(..., help="The player's profile slug/ID from their start.gg URL"),
    game_id: str = typer.Argument(..., help="Game ID to get results for")
):
    """Show a player's recent tournament results."""
    try:
        # First lookup the player's ID using their discriminator slug
        with console.status(f"[bold green]Looking up player ID for {player_slug}..."):
            player_id = lookup_player_id(player_slug, startgg.smash.header, startgg.smash.auto_retry)
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
    except Exception as e:
        console.print(f"[red]Error:[/] {str(e)}")
        raise typer.Exit(code=1)

@player_app.command(name="sets")
def player_sets(
    player_slug: str = typer.Argument(..., help="The player's profile slug/ID from their start.gg URL"),
    game_id: str = typer.Argument(..., help="Game ID to get sets for")
):
    """Show a player's recent tournament sets."""
    try:
        with console.status("[bold green]Fetching player data...") as status:
            # First lookup the player's ID using their discriminator slug
            player_id = lookup_player_id(player_slug, startgg.smash.header, startgg.smash.auto_retry)
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

            # Update status message
            status.update(status="[bold green]Finding most recent event...")

            # Get placements to find the most recent event and display player info
            variables = {"playerId": player_id, "videogameId": str(game_id_int)}
            response = run_query(PLAYER_RECENT_PLACEMENTS_QUERY, variables, startgg.smash.header, startgg.smash.auto_retry)

            # Display player info before showing sets
            create_player_info_panel(response)

            if (response and 'data' in response and
                response['data'].get('player') and
                response['data']['player'].get('recentStandings')):

                standings = response['data']['player']['recentStandings']
                if standings:
                    recent_event = standings[0]['entrant']['event']
                    event_id = recent_event['id']
                    is_online = recent_event['isOnline']

                    # Update status message
                    status.update(status="[bold green]Fetching sets for most recent event...")

                    variables = {
                        "playerId": player_id,
                        "isOnline": is_online,
                        "eventId": [event_id]
                    }
                    sets_response = run_query(PLAYER_SETS_QUERY, variables, startgg.smash.header, startgg.smash.auto_retry)
                    create_sets_table(sets_response)
                else:
                    console.print("[yellow]No recent events found[/]")
            else:
                console.print("[red]Could not find player's recent events[/]")
    except Exception as e:
        console.print(f"[red]Error:[/] {str(e)}")
        raise typer.Exit(code=1)
