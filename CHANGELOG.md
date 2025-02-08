# Changelog

All notable changes to this project will be documented in this file.

## [v2025.02.08-1] - 2025-02-08
### Changed
- Updated the `troubleshoot` command to provide more detailed information about configuration issues.
- Added support for Memos v0.24.0 API changes.

### Fixed
- Fix issue with Bluesky posts not being properly imported.
- Fixed issue #1 from the GitHub repository! Thanks @vnl for the feedback!

## [v2025.01.26-1] - 2025-01-26
### Added
- ⭐️ Support for Bluesky through the bluesky2memos command.
- Added support for --config-path option.
- Add translations for many languages (fr, de, es, it, pt, nl, pl, ru, cs, zh_CN, zh_TW, ja, ko).
- Add i18n_utils.py to extract and compile translations.

### Changed
- Fix minor date issue when importing resources (mastodon).
- Reorganized the project structure (added Converter classes to offload service-specific logic).

## [v2025.01.14-1] - 2025-01-14
### Added
- Initial release of the project.
- Basic functionality to copy posts from Mastodon to Memos.
- User authentication and authorization.
- Command-line interface for initiating migrations.
- Logging and error handling mechanisms.