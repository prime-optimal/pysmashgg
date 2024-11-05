# Changelog

All notable changes to this project will be documented in this file.

## [1.7.0] - 2024-11-05

### Added
- Enhanced tournament metadata display:
  - Added tournament URL display using tournament slug
  - Added tournament organizer name and ID display
  - Added support for additional metadata fields in SHOW_QUERY:
    - Social media links (discord, facebook)
    - Tournament rules
    - Publishing status
    - Stream information
    - Tournament images

### Fixed
- Fixed TypeError in search command's select feature when viewing tournament results
- Added proper null checks for optional tournament metadata fields
- Improved error handling for missing tournament organizer information

### Changed
- Updated SHOW_QUERY to include comprehensive tournament metadata
- Enhanced show_filter function to handle new metadata fields
- Improved tournament info display organization and formatting
- Modified results command to handle optional metadata fields
- Updated documentation with new metadata display features

## [1.6.0] - 2024-10-23

### Added
- New tournament search by video game functionality
  - Added GET_VIDEOGAME_ID_QUERY to find game IDs
  - Added SHOW_BY_VIDEOGAME_QUERY for tournament search
  - Added new --game option to search command
- New videogame_filters.py module for handling game-related responses
- Enhanced debug output for troubleshooting
- Added date filtering for tournament searches by game
  - Tournaments are now filtered to show only those within the next week by default
  - Added date range parameters to tournament search queries
  - Improved sorting to show nearest tournaments first

### Changed
- Updated tournament formatter to handle game search results
- Improved location display to show "Online" for online tournaments
- Enhanced search command with better error handling and feedback
- Modified tournament search to prioritize upcoming events
- Updated documentation and help text to reflect new date filtering behavior

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
