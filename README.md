# profile-activity-collector

Local-first social profile activity ingestion and reporting tools for Facebook, X, and LinkedIn.

This repository collects user-owned account export data and permitted official API data, normalizes it into a shared activity schema, stores it in local SQLite databases, and produces local JSON, CSV, and Markdown outputs.

## Contents

- [What This Project Does](#what-this-project-does)
- [Privacy And Compliance](#privacy-and-compliance)
- [Repository Layout](#repository-layout)
- [Supported Platforms](#supported-platforms)
- [Setup](#setup)
- [Platform CLI Usage](#platform-cli-usage)
- [Development](#development)
- [Testing](#testing)
- [Spec-Driven Workflow](#spec-driven-workflow)
- [Roadmap And Changelog](#roadmap-and-changelog)

## What This Project Does

- Imports user-owned social account archives.
- Optionally imports from official platform APIs when valid permissions are configured.
- Normalizes records into a common `Activity` shape.
- Stores normalized records, import runs, profile records, and raw source items in SQLite.
- Preserves raw item provenance for auditability.
- Deduplicates raw source items with stable hashes.
- Exports normalized activity to JSON and CSV.
- Generates Markdown summary reports.
- Provides fixture-driven tests for representative archive shapes.

## What This Project Does Not Do

- It does not scrape private third-party data.
- It does not bypass authentication, privacy controls, access restrictions, rate limits, bot detection, or platform protections.
- It does not automate posting, growth workflows, surveillance, data resale, or unauthorized sharing.
- It does not require cloud services for core ingestion, storage, or reporting.
- It does not commit or ship personal data.

## Privacy And Compliance

This project may process sensitive personal data. Keep imports, local databases, exports, reports, and credentials private.

Rules for safe use:

- Ingest only data you are authorized to access and process.
- Prefer account archive imports as the baseline source.
- Use official APIs only with valid permissions and platform-compliant scopes.
- Store API credentials only in local environment variables.
- Never commit `.env` files, platform exports, SQLite databases, generated reports containing personal data, or access tokens.
- Review generated exports before sharing them.

The root `.gitignore` and platform `.gitignore` files exclude common local data and credential paths, but the user is still responsible for safe handling.

## Repository Layout

```text
profile-activity-collector/
  profile_activity_core/          Shared models, database, validation, analytics, reports
  facebook-activity-logger/       Facebook-specific CLI, parsers, importers, tests
  x-activity-logger/              X-specific CLI, parsers, importers, tests
  linkedin-activity-logger/       LinkedIn-specific CLI, parsers, importers, tests
  tests/                          Shared core tests
  scripts/run_tests.py            Runs each platform test suite in isolation
  .github/specs/                  Lightweight feature specs for larger changes
  .specify/memory/constitution.md Project guardrails for AI-assisted work
  spec.md                         Project specification
  future-upgrades.md              Roadmap
  CHANGELOG.md                    Human-readable change log
```

## Supported Platforms

| Platform | Archive import | API import | Primary import command |
| --- | --- | --- | --- |
| Facebook | JSON-first Download Your Information exports | Meta Graph API, if permitted | `import-export` |
| X | X account archives, including JS-wrapper archive files | Official X API, if permitted | `import-archive` |
| LinkedIn | CSV and JSON LinkedIn data archives | LinkedIn API, if permitted | `import-archive` |

Each platform has its own README with platform-specific data download and credential notes:

- [Facebook Activity Logger](facebook-activity-logger/README.md)
- [X Activity Logger](x-activity-logger/README.md)
- [LinkedIn Activity Logger](linkedin-activity-logger/README.md)

## Setup

Use Python 3.11 or newer.

Create a virtual environment from the repository root:

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -e ".[dev]"
```

This installs the shared `profile_activity_core` package and development dependencies from [pyproject.toml](pyproject.toml).

If you only want to run one platform in isolation, you can still install that platform's pinned requirements:

```bash
cd x-activity-logger
python -m pip install -r requirements.txt
```

The root editable install is preferred for development because it includes the shared core package and test runner.

## Platform CLI Usage

Run platform commands from that platform's directory. Each platform CLI uses its local `.env` file when present.

### Facebook

```bash
cd facebook-activity-logger
cp .env.example .env
python -m src.main init-db
python -m src.main import-export --path ./data/imports/facebook-export
python -m src.main list-activity --limit 100
python -m src.main export-json --output ./data/exports/activity.json
python -m src.main export-csv --output ./data/exports/activity.csv
python -m src.main report --output ./data/reports/activity-summary.md
```

Optional Graph API import:

```bash
python -m src.main import-graph --since 2025-01-01
```

Set `FACEBOOK_ACCESS_TOKEN` in `facebook-activity-logger/.env` before using Graph API import.

### X

```bash
cd x-activity-logger
cp .env.example .env
python -m src.main init-db
python -m src.main import-archive --path ./data/imports/x-archive
python -m src.main list-activity --limit 100
python -m src.main export-json --output ./data/exports/activity.json
python -m src.main export-csv --output ./data/exports/activity.csv
python -m src.main report --output ./data/reports/activity-summary.md
```

Optional X API import:

```bash
python -m src.main import-api --since 2025-01-01
```

Set `X_API_BEARER_TOKEN` and `X_USER_ID` in `x-activity-logger/.env` before using API import.

### LinkedIn

```bash
cd linkedin-activity-logger
cp .env.example .env
python -m src.main init-db
python -m src.main import-archive --path ./data/imports/linkedin-archive
python -m src.main list-activity --limit 100
python -m src.main export-json --output ./data/exports/activity.json
python -m src.main export-csv --output ./data/exports/activity.csv
python -m src.main report --output ./data/reports/activity-summary.md
```

Optional LinkedIn API import:

```bash
python -m src.main import-api --since 2025-01-01
```

Set `LINKEDIN_ACCESS_TOKEN` and `LINKEDIN_PERSON_URN` in `linkedin-activity-logger/.env` before using API import.

## Configuration

Each platform loads environment variables from its own `.env` file.

Common setting:

- `DATABASE_PATH`: optional path to the SQLite database. Relative paths are resolved from the platform directory.

Platform API settings:

- Facebook: `FACEBOOK_ACCESS_TOKEN`
- X: `X_API_BEARER_TOKEN`, `X_USER_ID`
- LinkedIn: `LINKEDIN_ACCESS_TOKEN`, `LINKEDIN_PERSON_URN`

For local smoke tests without writing to the default platform DB path, override `DATABASE_PATH`:

```bash
DATABASE_PATH=/tmp/x-activity.db python -m src.main init-db
```

## Normalized Activity Schema

All platforms normalize records into this shape:

```json
{
  "id": "",
  "source": "",
  "activity_type": "",
  "title": "",
  "body": "",
  "url": "",
  "created_at": "",
  "updated_at": "",
  "actor": "",
  "target": "",
  "metadata": {}
}
```

SQLite tables:

- `activities`
- `imports`
- `profiles`
- `raw_items`

Shared schema and persistence behavior live in `profile_activity_core`.

## Development

Install from the repository root:

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -e ".[dev]"
```

Project conventions:

- Put shared behavior in `profile_activity_core`.
- Keep platform code focused on parsers, importers, API clients, and thin CLI adapters.
- Add parser/importer fixtures under the relevant platform's `tests/fixtures/`.
- Keep tests credential-free and personal-data-free.
- Preserve backward-compatible platform CLI commands unless a breaking change is explicitly planned.

## Testing

Run shared core tests:

```bash
python -m pytest -q
```

Run every platform test suite in isolated subprocesses:

```bash
python scripts/run_tests.py
```

The platform test runner intentionally runs each platform from its own directory so each local `src` package resolves correctly.

Current fixture coverage includes:

- Facebook JSON export examples for comments and posts.
- X JS-wrapper archive examples and multi-list JSON archive behavior.
- LinkedIn CSV and JSON archive examples.
- Raw item dedupe checks for repeated imports.

## Spec-Driven Workflow

Medium-to-large features should start from a lightweight feature spec in [.github/specs/](.github/specs/). The standing project guardrails live in [.specify/memory/constitution.md](.specify/memory/constitution.md).

Use specs for:

- Shared core changes
- Importer state or schema changes
- CLI behavior changes across platforms
- Local API/dashboard work
- Plugin architecture
- AI, semantic search, recommendation, or automation features

Specs are optional for:

- Small fixture additions
- Simple bug fixes
- Minor documentation edits
- Mechanical refactors with no behavior change

Useful spec files:

- [Spec workflow README](.github/specs/README.md)
- [Feature spec template](.github/specs/template.md)
- [Improved CLI UX seed spec](.github/specs/improved-cli-ux/spec.md)
- [Project constitution](.specify/memory/constitution.md)

## Roadmap And Changelog

- [Project specification](spec.md)
- [Future upgrades roadmap](future-upgrades.md)
- [Changelog](CHANGELOG.md)

The roadmap describes planned work. The changelog records completed repository changes.

## Current Limitations

- CLI filtering and pagination are planned but not fully implemented yet.
- Invalid-record persistence is planned; current validation rejects invalid activities in strict database paths.
- Incremental imports are partially prepared through dedupe behavior but do not yet skip unchanged files before parsing.
- API importers are intentionally conservative and depend on valid platform permissions.
- Dashboard, local API, plugin architecture, AI summarization, and semantic search remain future work.
