# Changelog

All notable changes to this project will be documented in this file.

## [1.12.0] - 2024-11-07

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

[Previous content remains exactly the same]
