# pysmashgg

A Python wrapper for the start.gg API (formerly smash.gg).

## Installation

```bash
pip install pysmashgg
```

## Development Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/pysmashgg.git
cd pysmashgg
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up pre-commit hooks:
```bash
pre-commit install
```

This will automatically run tests before each commit to ensure code quality.

5. Create a .env file with your start.gg API key:
```bash
echo "KEY=your_api_key_here" > .env
```

## Running Tests

Tests can be run manually with:
```bash
python -m unittest tests/tests.py
```

Tests will also run automatically before each commit thanks to pre-commit hooks.

## Usage

### Basic Examples

```python
import os
from dotenv import load_dotenv
import pysmashgg

# Load API key from environment
load_dotenv()
smash = pysmashgg.SmashGG(os.getenv('KEY'))

# Get tournament info
tournament = smash.tournament_show("can-opener-series-vol-140-adventures-of-buss-ass")

# Get player info
player = smash.player_show_info("06989544")

# Get tournament results
results = smash.tournament_show_results("can-opener-series-vol-140-adventures-of-buss-ass")
```

### Command Line Interface

The package includes a command-line interface for common operations:

```bash
# Show tournament results
python startgg.py results can-opener-series-vol-140-adventures-of-buss-ass

# Export tournament results to files
python startgg.py results can-opener-series-vol-140-adventures-of-buss-ass --json results.json --csv results.csv

# Show player results (multiple identifier formats supported)
python startgg.py results user/b1008ff3                # With user/ prefix
python startgg.py results b1008ff3                     # Without user/ prefix
python startgg.py results 156685                       # Using player ID

# Show player results for a specific game
python startgg.py results user/b1008ff3 --game 43868
python startgg.py results 156685 --game 43868

# Show player info (multiple identifier formats supported)
python startgg.py player info user/b1008ff3            # With user/ prefix
python startgg.py player info b1008ff3                 # Without user/ prefix
python startgg.py player info 156685                   # Using player ID

# Show player results (multiple identifier formats supported)
python startgg.py player results user/b1008ff3
python startgg.py player results b1008ff3
python startgg.py player results 156685

# Show player results for a specific game
python startgg.py player results user/b1008ff3 --game 43868
python startgg.py player results 156685 --game 43868

# Show player sets from most recent event (multiple identifier formats supported)
python startgg.py player sets user/b1008ff3 43868
python startgg.py player sets b1008ff3 43868
python startgg.py player sets 156685 43868

# Search for tournaments or players
python startgg.py search --player your-player-slug
python startgg.py search --game "Street Fighter 6"

# Search for tournaments by owner ID
python startgg.py search --owner 123456

# Search using tournament slug to find more by same organizer
python startgg.py search --tournament can-opener-series-vol-140-adventures-of-buss-ass

# Search with interactive selection
python startgg.py search --game "Street Fighter 6" --select
```

### Player Results Features

The player results command now provides comprehensive tournament statistics:

```bash
# Show all tournament results with statistics
python startgg.py player results your-player-slug
python startgg.py player results 156685  # Using player ID directly
```

This will display:
- Player information panel with Player ID
- Recent tournament placements table
- Tournament statistics:
  * Number of 1st, 2nd, and 3rd place finishes
  * Online vs Offline tournament percentages
- Tournaments by game summary with game IDs
- Available games with their IDs

You can also directly view results for a specific game:
```bash
python startgg.py player results your-player-slug --game 43868
python startgg.py player results 156685 --game 43868  # Using player ID directly
```

All player-related commands now support three identifier formats:
1. Player slugs with "user/" prefix (e.g., user/b1008ff3)
2. Player slugs without prefix (e.g., b1008ff3)
3. Numerical player IDs (e.g., 156685)

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests to ensure everything works (`python -m unittest tests/tests.py`)
5. Commit your changes (tests will run automatically)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE.md file for details.
