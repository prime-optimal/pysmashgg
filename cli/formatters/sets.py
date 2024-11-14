"""Sets display formatting module."""

from datetime import datetime
from rich.table import Table
from .. import console

def create_sets_table(sets_data):
    """Format and display player's sets in a table.
    
    Args:
        sets_data: Response data from the sets query
        
    Returns:
        None
    """
    try:
        if not sets_data or 'data' not in sets_data or not sets_data['data'].get('player'):
            console.print("[red]No sets data found[/]")
            return

        player = sets_data['data']['player']
        sets = player.get('sets', {}).get('nodes', [])

        if not sets:
            console.print("[yellow]No sets found for this player[/]")
            return

        # Create sets table
        table = Table(title=f"Sets for {player['gamerTag']}")
        table.add_column("Date & Time", style="cyan", justify="right")
        table.add_column("Round", style="green")
        table.add_column("Opponent", style="yellow")
        table.add_column("Score", justify="center")
        table.add_column("Event", style="blue")

        # Sort sets by completedAt timestamp in ascending order
        sorted_sets = sorted(sets, key=lambda x: x.get('completedAt', 0))

        for set_data in sorted_sets:
            # Format date and time
            date_time = "N/A"
            if set_data.get('completedAt'):
                date_time = datetime.fromtimestamp(set_data['completedAt']).strftime('%Y-%m-%d %I:%M %p')

            # Format round text
            round_text = set_data.get('fullRoundText', 'Unknown Round')

            # Get opponent and scores
            slots = set_data.get('slots', [])
            opponent_name = "N/A"
            score = "DQ"

            if len(slots) == 2:  # Only process if we have exactly 2 slots
                player_score = None
                opponent_score = None

                # First find the opponent's name and both scores
                for slot in slots:
                    entrant = slot.get('entrant', {})
                    entrant_name = entrant.get('name', '')
                    if entrant and entrant_name:
                        score_value = slot.get('standing', {}).get('stats', {}).get('score', {}).get('value')
                        # Check if this is our player by looking for their gamerTag in the entrant name
                        if player['gamerTag'] in entrant_name:
                            player_score = score_value
                        else:
                            opponent_name = entrant_name
                            opponent_score = score_value

                # Format score if we have both scores
                if player_score is not None and opponent_score is not None:
                    # Handle DQ case
                    if opponent_score == -1:
                        score = "[green]W - DQ[/]"
                    elif player_score == -1:
                        score = "[red]DQ - W[/]"
                    # Handle normal scores
                    elif player_score > opponent_score:
                        score = f"[green]{player_score} - {opponent_score}[/]"
                    elif player_score < opponent_score:
                        score = f"[red]{player_score} - {opponent_score}[/]"
                    else:
                        score = f"{player_score} - {opponent_score}"

            # Get event info
            event = set_data.get('event', {})
            tournament = event.get('tournament', {})
            event_name = f"{tournament.get('name', 'Unknown Tournament')}"

            # Add row to table
            table.add_row(
                date_time,
                round_text,
                opponent_name,
                score,
                event_name
            )

        console.print(table)

    except Exception as e:
        console.print(f"[red]Error displaying sets:[/] {str(e)}")
