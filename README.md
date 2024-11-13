# Start.gg Tournament Results CLI

A command-line interface for fetching and displaying tournament information from Start.gg (formerly Smash.gg).

## Requirements

- Python 3.6+
- `pysmashgg` library
- `python-dotenv` library
- `typer` library
- `rich` library

## Installation

1. Clone this repository
2. Install the required libraries:
   ```
   pip install pysmashgg python-dotenv "typer[all]"
   ```
3. Create a `.env` file in the project root and add your Start.gg API key:
   ```
   KEY=your_api_key_here
   ```

## Usage

The CLI provides two main commands: `search` and `results`.

### Search for Tournaments

You can search for tournaments in three ways:

1. Using a tournament slug to find the organizer and their tournaments:
```bash
python startgg.py search --tournament <tournament-slug>
```

2. Directly using the tournament organizer's ID:
```bash
python startgg.py search --owner <owner-id>
```

3. By game name to find upcoming tournaments:
```bash
python startgg.py search --game "Street Fighter 6"
```

Search options:
- `--tournament`, `-t`: Search using a tournament slug to find the organizer
- `--owner`, `-o`: Search directly with a tournament organizer's ID
- `--game`, `-g`: Search for tournaments by game name
- `--page`, `-p`: Page number for results (default: 1)
- `--limit`, `-l`: Number of tournaments to display (default: 10)
- `--select`, `-s`: Interactively select a tournament to view its results

Examples:
```bash
# Find tournaments by a known tournament slug
python startgg.py search --tournament tns-street-fighter-6-69

# Display first 5 tournaments for owner ID 161429
python startgg.py search --owner 161429 --limit 5

# Search with interactive selection
python startgg.py search --owner 161429 --select

# View next page of results
python startgg.py search --owner 161429 --page 2

# Find upcoming Street Fighter 6 tournaments
python startgg.py search --game "Street Fighter 6"
```

The search command displays:
- Tournament name and slug
- Event date
- Location (shows "Online" for online tournaments)
- Number of entrants

When using the `--select` option, you can choose a tournament from the list to immediately view its results.


### Get Tournament Results

The results command can be used in two ways:

1. View tournament results:
```bash
python startgg.py results <tournament-slug> [OPTIONS]
```

2. View player tournament placements:
```bash
python startgg.py results --player <player-id> --game <game-id>
```

Tournament results options:
- `--json`, `-j`: Export results in JSON format
- `--csv`, `-c`: Export results in CSV format
- `--txt`, `-t`: Export results in TXT format

Player results options:
- `--player`, `-p`: Player profile ID from their start.gg URL (e.g., "06989544" from start.gg/user/06989544)
- `--game`, `-g`: Game ID (required with --player, e.g., "38" for King of Fighters XIV)

Examples:
```bash
# View tournament results
python startgg.py results tns-street-fighter-6-69

# Export tournament results to JSON
python startgg.py results tns-street-fighter-6-69 --json results.json

# View player's tournament placements
python startgg.py results --player 06989544 --game 38
```

[Rest of the file remains the same until "Output" section, then update that section:]

## Output

The CLI provides rich, formatted output including:

For search results:
- Tournament names and slugs
- Event dates and locations
- Number of entrants
- Tournament organizer information (when searching by tournament slug)
- Interactive selection option

For tournament results:
1. Tournament information:
   - Name and direct URL to tournament page
   - Location (city, state or "Online")
   - Date range
   - Number of entrants
   - Tournament organizer name and ID
2. List of events in the tournament
3. Top 8 results for each event, including:
   - Player placement and name
   - Twitter handle (with @ symbol)
   - Twitch username
   - Total participant count

For player results:
1. Player information:
   - Gamer tag and prefix
   - Player ID
   - Location
2. Recent tournament placements:
   - Tournament name and event
   - Placement (with medals for top 3: 🥇, 🥈, 🥉)
   - Number of entrants
   - Date
   - Online/Offline indicator

