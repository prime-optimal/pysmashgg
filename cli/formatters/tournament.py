"""Tournament table formatting utilities."""

from datetime import datetime
from rich.table import Table

def create_tournament_table(tournaments, owner_id):
    """Create a Rich table for displaying tournaments."""
    table = Table(title=f"Tournaments by Owner ID: {owner_id}")
    table.add_column("#", style="cyan", justify="right")
    table.add_column("Name", style="green")
    table.add_column("Date", style="yellow")
    table.add_column("Location", style="blue")
    table.add_column("Entrants", justify="right", style="magenta")
    table.add_column("Slug", style="white", overflow="fold")

    for idx, tournament in enumerate(tournaments, 1):
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

    return table
