# Changelog

All notable changes to this project will be documented in this file.

## [1.5.2] - 2024-10-23

### Changed
- Improved location display to show "Online" instead of "None, None" when no city/state is available
- Updated location formatting in both search results and tournament details

## [1.5.1] - 2024-10-23

### Added
- Debug output for tournament data structure in search command
- Comprehensive code documentation and comments

### Fixed
- Entrants count display in tournament search results
- Field mapping in tournament formatter

## [1.5.0] - 2024-10-22

### Added
- Enhanced search functionality:
  - Search by tournament slug to find organizer
  - Get tournament organizer information
  - Interactive tournament selection
- Custom GraphQL query for tournament owner information
- Improved error handling for search operations
- Updated documentation with new search features

### Changed
- Search command now supports both owner ID and tournament slug
- Improved search results display with more tournament details
- Enhanced help text with more examples and usage information

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
