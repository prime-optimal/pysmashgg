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

# Show player info (no game ID needed)
python startgg.py player info 06989544

# Show player results (requires game ID, e.g. 43868 for Street Fighter 6)
python startgg.py player results 06989544 43868

# Show player sets from most recent event
python startgg.py player sets 06989544 43868

# Search for tournaments or players
python startgg.py search --player 06989544
python startgg.py search --game "Street Fighter 6"

# Search for tournaments by owner ID
python startgg.py search --owner 123456

# Search using tournament slug to find more by same organizer
python startgg.py search --tournament can-opener-series-vol-140-adventures-of-buss-ass

# Search with interactive selection
python startgg.py search --game "Street Fighter 6" --select
```

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
