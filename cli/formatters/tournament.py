"""Tournament table formatting utilities."""

from datetime import datetime
from rich.table import Table

def create_tournament_table(tournaments, title):
    """Create a Rich table for displaying tournaments.
    
    Args:
        tournaments: List of tournament dictionaries containing tournament information
                    Each tournament should have: name, startTimestamp, city, state, entrants, slug
        title: Title for the table (e.g., Owner ID or Game name)
    
    Returns:
        Rich Table object containing formatted tournament information with columns:
        - #: Index number
        - Name: Tournament name
        - Date: Tournament start date
        - Location: City, State or "Online" if no location
        - Entrants: Number of participants
        - Slug: Tournament slug for API reference
    """
    table = Table(title=f"Tournaments by {title}")
    table.add_column("#", style="cyan", justify="right")
    table.add_column("Name", style="green")
    table.add_column("Date", style="yellow")
    table.add_column("Location", style="blue")
    table.add_column("Entrants", justify="right", style="magenta")
    table.add_column("Slug", style="white", overflow="fold")

    for idx, tournament in enumerate(tournaments, 1):
        # Convert timestamp to readable date
        start_date = datetime.fromtimestamp(tournament.get('startTimestamp', 0)).strftime('%Y-%m-%d')
        
        # Format location, showing "Online" if no city/state available
        city = tournament.get('city')
        state = tournament.get('state')
        location = f"{city}, {state}" if city and state else "Online"
        
        # Get entrants count, defaulting to N/A if not available
        entrants = str(tournament.get('entrants', 'N/A'))
        
        table.add_row(
            str(idx),
            tournament['name'],
            start_date,
            location,
            entrants,
            tournament['slug']
        )

    return table
