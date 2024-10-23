# Changelog

All notable changes to this project will be documented in this file.

## [1.4.0] - 2024-01-14

### Added
- New CLI interface using Typer and Rich libraries
- Search command to find tournaments by owner ID
- Improved formatting with colored output and tables
- Progress indicators for long-running operations
- Better help text and command documentation

### Changed
- Renamed main script from app.py to startgg.py
- Restructured commands into a more organized CLI
- Updated documentation with new command structure
- Improved error handling and user feedback

### Removed
- Old app.py script in favor of new CLI structure

## [1.3.0] - 2024-01-10

### Added
- Export functionality for results in JSON, CSV, and TXT formats
- Command-line flags for export options (-j, -c, -t)
- Detailed help information accessible via -h flag
- Display of total number of participants for each event

### Changed
- Improved tournament information display format
- Replace tournament slug with full tournament name in output
- Enhanced readability of Top 8 results output

### Fixed
- Error handling for API responses

## [1.2.0] - 2023-06-01

### Added
- Support for fetching results from multiple events in a tournament

### Changed
- Improved error handling and user feedback

## [1.1.0] - 2023-05-15

### Added
- Command-line interface for specifying tournament slug

### Changed
- Refactored code for better modularity

## [1.0.0] - 2023-05-01

### Added
- Initial release
- Basic functionality to fetch Top 8 results from a Smash.gg tournament
