# Changelog

All notable changes to this project will be documented in this file.

## [1.4.0] - 2024-10-23

### Changed
- Refactored CLI code into a dedicated package structure for better maintainability
  - Separated commands into individual modules (search.py, results.py)
  - Created dedicated formatters for table display
  - Isolated export functionality
  - Improved error handling for API key configuration
- Improved code organization and separation of concerns
- Simplified main entry point (startgg.py)

## [1.3.0] - 2024-09-15

### Added
- Added support for searching tournaments by owner ID
- Added interactive tournament selection with --select flag
- Added CSV export functionality for tournament results
- Added TXT export functionality for tournament results

### Changed
- Improved error handling for API requests
- Enhanced tournament information display
- Updated documentation with new features

## [1.2.0] - 2024-08-20

### Added
- Added JSON export functionality for tournament results
- Added support for multiple events in tournaments
- Added tournament date range display

### Changed
- Improved table formatting for better readability
- Enhanced error messages for better user feedback

## [1.1.0] - 2024-07-10

### Added
- Added support for tournament search by slug
- Added rich table display for tournament results
- Added pagination support for tournament listings

### Changed
- Improved command-line interface
- Enhanced error handling
- Updated documentation

## [1.0.0] - 2024-06-01

### Added
- Initial release
- Basic tournament results fetching
- Command-line interface
- Tournament search functionality
