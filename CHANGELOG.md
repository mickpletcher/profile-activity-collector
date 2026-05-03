# Changelog

All notable repository-level changes are recorded here.

This project currently uses an unreleased changelog while the baseline is still forming.

## Unreleased

### Added

- Added shared `profile_activity_core` package for common models, SQLite persistence, validation, analytics, and report/export helpers.
- Added top-level Python packaging via `pyproject.toml`.
- Added `scripts/run_tests.py` to run each platform test suite in isolation.
- Added shared core tests under `tests/`.
- Added fixture-based parser/importer tests for Facebook, X, and LinkedIn.
- Added representative archive fixtures under each platform's `tests/fixtures/`.
- Added raw-item hash dedupe support in the shared database layer.
- Added lightweight spec-driven workflow documentation:
  - `.specify/memory/constitution.md`
  - `.github/specs/README.md`
  - `.github/specs/template.md`
  - `.github/specs/improved-cli-ux/spec.md`
- Added detailed top-level README instructions for setup, CLI usage, development, testing, and spec workflow.

### Changed

- Replaced duplicated platform model, database, analytics, and report/export implementations with compatibility shims around `profile_activity_core`.
- Updated platform API importers with pagination-aware loops where platform responses expose pagination.
- Improved source item ID handling in archive parsers for more stable activity identities.
- Updated parser type inference to use file names instead of full paths, avoiding accidental matches from parent directory names.
- Expanded `future-upgrades.md` to reflect current shared-core architecture, partially implemented foundation work, and revised priorities.

### Fixed

- Fixed raw source item duplication on repeated imports by adding stable raw-item hashes and a unique raw item identity index.
- Fixed LinkedIn activity type inference bug where parent folder names could cause `posts.csv` to be classified as `profile_changes`.
- Fixed X JSON archive parsing so files containing multiple top-level lists are fully parsed instead of returning only the first list.

### Verified

- Shared core tests pass with `python -m pytest -q`.
- Platform suites pass with `python scripts/run_tests.py`.
- Platform `init-db` smoke tests pass with temporary database paths.
