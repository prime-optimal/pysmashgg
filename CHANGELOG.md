# Changelog

All notable changes to this project will be documented in this file.

## [1.13.0] - 2024-11-15

### Added
- Added automated testing workflow:
  - Pre-commit hooks for running tests before commits
  - Code quality checks (whitespace, YAML, etc.)
  - Updated requirements.txt with development dependencies
  - Enhanced test coverage for new features

### Changed
- Reorganized code structure:
  - Created centralized queries.py for all GraphQL queries
  - Updated all modules to use centralized queries
  - Improved error handling for API rate limits
  - Added delay between API calls to prevent 503 errors
- Enhanced player info command:
  - Removed game ID requirement for basic player info
  - Improved player info display with profile URL and social media
  - Better handling of league event dates
- Updated documentation:
  - Added development setup instructions
  - Included pre-commit hook setup
  - Enhanced contribution guidelines

### Fixed
- Fixed date display for league events (now shows event date instead of league start date)
- Fixed API rate limit handling with automatic retry and delay
- Fixed error handling for tournament results with many events

## [1.12.0] - 2024-11-14

### Changed
- Enhanced sets display functionality:
  - Improved score formatting with proper DQ handling
  - Added colored "W - DQ" and "DQ - W" indicators
  - Fixed player identification across different events
  - Moved sets display logic to dedicated formatter module
  - Sets now sorted chronologically (earliest first)

## [1.11.0] - 2024-11-07

### Changed
- Refactored sets functionality:
  - Moved sets display logic to new formatter module
  - Improved sets table formatting with better date/time display
  - Enhanced opponent name and score display
  - Added colored scores (green for wins, red for losses)
  - Sets now sorted chronologically (earliest first)

## [1.10.0] - 2024-11-07

### Added
- Added player sets functionality:
  - New `--sets` flag to view player's recent sets
  - Integration with player results to show sets from most recent event
  - Detailed set information including round, score, and outcome
  - Support for both online and offline events
  - Added new PLAYER_SETS_QUERY for fetching set data

### Changed
- Enhanced results command with sets display capability
- Updated player queries to support set filtering by event
- Improved results display with set-specific formatting

## [1.9.0] - 2024-11-06

### Added
- Added player results functionality:
  - New `--player` option to view player tournament placements
  - Required `--game` option to specify the game ID
  - Results sorted by date (newest first)
  - Rich display of player info and placement details
  - Support for emoji medals (🥇, 🥈, 🥉) for top 3 placements

### Changed
- Updated results command to support both tournament and player results
- Added new GraphQL queries for player lookup and placements
- Enhanced results display with player location and prefix information

## [1.8.0] - 2024-11-06

### Added
- Added social media display in tournament results:
  - Twitter handles shown with @ symbol
  - Twitch usernames displayed in purple
  - Updated SHOW_LIGHTWEIGHT_RESULTS_QUERY to include social media data
  - Enhanced results table with social media columns

### Changed
- Modified results display to show player social media information
- Updated results filter to process social media authorizations
- Improved table formatting with color-coded social media handles

## [1.7.0] - 2024-11-05

### Added
- Added tournament search by game name
- Added date filtering for tournament searches
- Added support for searching tournaments by owner ID
- Added player search functionality

### Changed
- Enhanced tournament metadata display
- Improved search command with multiple options
- Updated documentation with new search features

## [1.6.0] - 2024-11-04

### Added
- New CLI structure using Typer framework
- Added search command with multiple options
- Enhanced help text and command documentation

### Changed
- Refactored CLI code into dedicated package
- Improved error handling and user feedback
- Updated command structure for better usability

## [1.5.0] - 2024-11-03

### Added
- Support for league tournaments
- Enhanced tournament metadata display
- Improved location information handling

### Changed
- Updated tournament queries for better data retrieval
- Enhanced error handling for API responses
- Improved documentation

## [1.4.0] - 2024-11-02

### Added
- Comprehensive code documentation
- Enhanced search functionality
- Improved location display in results

### Changed
- Reorganized code structure for better maintainability
- Updated API response handling
- Enhanced error messages

## [1.3.0] - 2024-10-18

### Added
- Export functionality for results in JSON CSV and TXT formats
- Command-line flags for export options (-j -c -t)
- Detailed help information accessible via -h flag
- Display of total number of participants for each event

### Changed
- Improved tournament information display format
- Replace tournament slug with full tournament name in output
- Enhanced readability of Top 8 results output

### Fixed
- Error handling for API responses
