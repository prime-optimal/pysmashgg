"""Results table formatting utilities."""

from rich.table import Table

def create_results_table(event_name, top_8, total_players):
    """Create a Rich table for displaying tournament results."""
    table = Table(title=f"{event_name} Top 8 ({total_players} players total)")
    table.add_column("Place", justify="right", style="cyan")
    table.add_column("Player", style="white")
    table.add_column("Twitter", style="blue")
    table.add_column("Twitch", style="purple")
    
    for player in top_8:
        twitter_handle = ""
        twitch_handle = ""
        if 'socials' in player:
            if 'twitter' in player['socials']:
                twitter_handle = f"@{player['socials']['twitter']}"
            if 'twitch' in player['socials']:
                twitch_handle = player['socials']['twitch']
            
        table.add_row(
            str(player['placement']), 
            player['name'],
            twitter_handle,
            twitch_handle
        )
    
    return table
