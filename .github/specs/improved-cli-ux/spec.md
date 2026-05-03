# Feature: Improved CLI UX

## Status

Draft

## Problem

The platform CLIs can initialize databases, import data, list recent activity, export all activity, and generate reports. However, `list-activity` and export workflows are currently coarse. Users cannot filter by source, activity type, date range, or text content, and large datasets have no offset/page controls. This makes manual inspection and repeatable local analysis harder as archives grow.

## Goals

- Add consistent filtering and pagination to platform CLIs.
- Keep query behavior shared in `profile_activity_core`.
- Preserve deterministic ordering for lists and exports.
- Support machine-readable JSON output and human-friendly table output.
- Keep existing CLI commands backward compatible.

## Non-Goals

- Do not add a dashboard or API as part of this feature.
- Do not introduce a full query DSL yet.
- Do not require cloud services or platform credentials.
- Do not change archive import behavior.

## User Workflows

### Filter Recent Activity

1. User runs `python -m src.main list-activity --type posts --limit 25`.
2. The CLI queries local SQLite through shared core helpers.
3. The CLI prints only matching records in deterministic order.

### Search Activity Text

1. User runs `python -m src.main list-activity --contains launch --format table`.
2. The CLI searches title, body, actor, target, URL, and metadata text where practical.
3. The CLI prints a readable local table without exposing secrets.

### Page Through Results

1. User runs `python -m src.main list-activity --limit 50 --offset 100`.
2. The CLI returns the third page of results using stable ordering.
3. Re-running the command against unchanged data returns the same records.

### Export A Filtered Slice

1. User runs `python -m src.main export-json --type comments --from-date 2024-01-01 --output comments.json`.
2. The export uses the same shared filter behavior as `list-activity`.
3. The output contains only matching records.

## Functional Requirements

- Add shared filter fields:
  - `source`
  - `activity_type`
  - `from_date`
  - `to_date`
  - `contains`
  - `limit`
  - `offset`
- Add shared query helpers in `profile_activity_core`, using parameterized SQL only.
- `list-activity` must support `--source`, `--type`, `--from-date`, `--to-date`, `--contains`, `--limit`, `--offset`, and `--format`.
- `--format` must support `json` and `table`; default remains JSON-compatible with current behavior unless explicitly changed.
- Export commands should use the same filter object where practical.
- Ordering must be deterministic: `created_at DESC, id ASC`.
- Invalid date inputs must fail with a clear CLI error.
- Unknown activity types should not crash query execution, but should return zero results unless matching rows exist.

## Data And Schema Impact

No schema migration is required. Query helpers should reuse existing indexed fields:

- `source`
- `activity_type`
- `created_at`

Optional future improvements may add FTS indexes, but this feature should use portable SQLite `LIKE` filters for now.

## Privacy And Compliance

- All filtering happens locally against the user's SQLite database.
- No data leaves the machine.
- Table output should avoid printing raw metadata by default.
- Commands must not require API credentials.
- Error messages must not include tokens or secret environment values.

## Implementation Plan

- Add a shared `ActivityFilter` dataclass in `profile_activity_core.query`.
- Add `Database.query_activities(filter)` and `Database.count_activities(filter)` methods.
- Add shared CLI option helpers where they can be used by all platform CLIs without import conflicts.
- Update each platform `src/main.py` to apply filters to `list-activity`.
- Extend JSON and CSV exports to accept optional filters.
- Add table formatting with a small internal formatter or optional `tabulate` dependency.
- Update README examples once the CLI behavior is implemented.

## Test Plan

- Add shared core tests for query filtering by source, type, date range, text, limit, and offset.
- Add platform CLI tests for `list-activity` filters using fixture imports.
- Add export tests for filtered JSON and CSV outputs.
- Add invalid date tests.
- Run:
  - `python -m pytest -q`
  - `python scripts/run_tests.py`

## Acceptance Criteria

- All platform `list-activity` commands support the shared filter flags.
- Filtered results are deterministic.
- Filter behavior is implemented once in shared core.
- Existing tests continue to pass.
- New tests cover source, type, date, text, limit, offset, and invalid input.
