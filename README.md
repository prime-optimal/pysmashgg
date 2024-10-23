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

The CLI provides two main commands:

### Search for Tournaments

Search for tournaments by owner ID:
```
python startgg.py search <owner-id>
```

Options:
- `--page`, `-p`: Page number for results (default: 1)
- `--limit`, `-l`: Number of tournaments to display (default: 10)

Example:
```
python startgg.py search 12345 --limit 20
```

### Get Tournament Results

Fetch and display Top 8 results for all events in a tournament:
```
python startgg.py results <tournament-slug>
```

Export options:
- `--json`, `-j`: Export results in JSON format
- `--csv`, `-c`: Export results in CSV format
- `--txt`, `-t`: Export results in TXT format

Example:
```
python startgg.py results tns-street-fighter-6-69 --json results.json
```

### Help

To see all available commands and options:
```
python startgg.py --help
```

For help with a specific command:
```
python startgg.py <command> --help
```

## Output

The CLI provides rich, formatted output including:
1. Tournament information (name, location, date, number of entrants)
2. List of events in the tournament
3. Top 8 results for each event, including the total number of participants

When using the search command, you'll see:
1. Tournament names and slugs
2. Dates and locations
3. Number of entrants
4. A tip showing how to view results for any listed tournament

## Contributing

Feel free to open issues or submit pull requests if you have suggestions for improvements or encounter any bugs.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
