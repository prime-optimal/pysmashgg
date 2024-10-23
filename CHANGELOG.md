# Changelog

All notable changes to this project will be documented in this file.

## [1.6.0] - 2024-10-23

### Added
- New tournament search by video game functionality
  - Added GET_VIDEOGAME_ID_QUERY to find game IDs
  - Added SHOW_BY_VIDEOGAME_QUERY for tournament search
  - Added new --game option to search command
- New videogame_filters.py module for handling game-related responses
- Enhanced debug output for troubleshooting

### Changed
- Updated tournament formatter to handle game search results
- Improved location display to show "Online" for online tournaments
- Enhanced search command with better error handling and feedback

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

[Earlier entries...]
