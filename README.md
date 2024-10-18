# Smash.gg Tournament Results Fetcher

This script fetches and displays Top 8 results for all events in a specified Smash.gg tournament. It also provides options to export the results in various formats.

## Requirements

- Python 3.6+
- `pysmashgg` library
- `python-dotenv` library

## Installation

1. Clone this repository
2. Install the required libraries:
   ```
   pip install pysmashgg python-dotenv
   ```
3. Create a `.env` file in the project root and add your Smash.gg API key:
   ```
   KEY=your_api_key_here
   ```

## Usage

Basic usage:
```
python app.py <tournament-slug>
```

Example:
```
python app.py tns-street-fighter-6-69
```

This will display the tournament information and Top 8 results for all events in the tournament.

### Export Options

You can export the results in different formats using the following flags:

- `-j` or `--json`: Export results in JSON format
- `-c` or `--csv`: Export results in CSV format
- `-t` or `--txt`: Export results in TXT format

Examples:
```
python app.py tns-street-fighter-6-69 -j results.json
python app.py tns-street-fighter-6-69 -c results.csv
python app.py tns-street-fighter-6-69 -t results.txt
```

### Help

To see all available options and get help, use the `-h` flag:
```
python app.py -h
```

## Output

The script will display:
1. Tournament information (name, location, date, number of entrants)
2. List of events in the tournament
3. Top 8 results for each event, including the total number of participants

If an export option is used, the results will be saved in the specified format.

## Contributing

Feel free to open issues or submit pull requests if you have suggestions for improvements or encounter any bugs.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
