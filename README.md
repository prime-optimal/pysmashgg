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

Fetch and display Top 8 results for all events in a tournament:
```bash
python startgg.py results <tournament-slug> [OPTIONS]
```

Export options:
- `--json`, `-j`: Export results in JSON format
- `--csv`, `-c`: Export results in CSV format
- `--txt`, `-t`: Export results in TXT format

Example:
```bash
python startgg.py results tns-street-fighter-6-69 --json results.json
```

### Help

To see all available commands and options:
```bash
python startgg.py --help
```

For help with a specific command:
```bash
python startgg.py search --help
python startgg.py results --help
```

## Output

The CLI provides rich, formatted output including:

For search results:
- Tournament names and slugs
- Event dates and locations
- Number of entrants
- Tournament organizer information (when searching by tournament slug)
- Interactive selection option

For tournament results:

1.  Tournament information:
   - Name and direct URL to tournament page
   - Location (city, state or "Online")
   - Date range
   - Number of entrants
   - Tournament organizer name and ID
2.  List of events in the tournament
3.  Top 8 results for each event, including:
   - Player placement and name
   - Twitter handle (with @ symbol)
   - Twitch username
   - Total participant count

## Export Formats

Results can be exported in three formats:

1. JSON:
   - Structured data format
   - Includes all event results
   - Ideal for programmatic use

2. CSV:
   - Comma-separated values
   - Easy to import into spreadsheets
   - One row per player placement

3. TXT:
   - Plain text format
   - Human-readable
   - Formatted similar to console output

## Contributing

Feel free to open issues or submit pull requests if you have suggestions for improvements or encounter any bugs.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
