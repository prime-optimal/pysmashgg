"""Results table formatting utilities."""

from rich.table import Table

def create_results_table(event_name, top_8, total_players):
    """Create a Rich table for displaying tournament results."""
    table = Table(title=f"{event_name} Top 8 ({total_players} players total)")
    table.add_column("Place", justify="right", style="cyan")
    table.add_column("Player", style="white")
    
    for player in top_8:
        table.add_row(str(player['placement']), player['name'])
    
    return table
