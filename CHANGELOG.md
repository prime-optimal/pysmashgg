# Changelog

All notable changes to this project will be documented in this file.

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
