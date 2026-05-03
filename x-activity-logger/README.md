# X Activity Logger (Compliant, Local-First)

This project is a compliant, local-first Python CLI for importing and analyzing your own X account activity data from permitted sources.

## Privacy Warning

This tool processes potentially sensitive personal account data. Keep all imported archives, database files, and generated reports local. Never commit personal data or credentials.

## What This Tool Does

- Imports your X account archive exports (primary source).
- Supports optional official X API import when valid permissions and rate limits allow it.
- Normalizes activity into a consistent event schema.
- Stores normalized events and raw source records in local SQLite.
- Exports normalized activity to JSON and CSV.
- Generates a markdown summary report.

## What This Tool Does Not Do

- Does not bypass authentication, privacy controls, access restrictions, or rate limits.
- Does not evade bot detection or platform protections.
- Does not scrape private data from other users.
- Does not automate prohibited platform behavior.

## Supported Sources

1. X data archive export files
2. Official X API where valid permissions exist
3. Manual import folder for downloaded JSON files

## Project Structure

```text
x-activity-logger/
  README.md
  requirements.txt
  .env.example
  src/
    main.py
    config.py
    database.py
    models.py
    importers/
      x_archive_importer.py
      x_api_importer.py
    parsers/
      json_parser.py
      js_archive_parser.py
    reports/
      markdown_report.py
      csv_export.py
      json_export.py
    analytics/
      activity_summary.py
      engagement_summary.py
  data/
    imports/
    exports/
    reports/
  tests/
    test_models.py
    test_database.py
    test_importer.py
```

## Setup

1. Create and activate a virtual environment.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Configure environment:

```bash
cp .env.example .env
```

If you plan to use API import, set `X_API_BEARER_TOKEN` and `X_USER_ID` in `.env`.

## Initialize Database

```bash
python -m src.main init-db
```

## How To Download Your X Archive Manually

1. Sign in to your X account.
2. Open account settings and privacy.
3. Find the data download/archive section.
4. Request your account archive and complete any required verification.
5. Download the archive when available.
6. Extract it to a local folder, for example `./data/imports/x-archive`.

## Import Archive Data

```bash
python -m src.main import-archive --path ./data/imports/x-archive
```

## Configure Official X API Access

1. Create and configure an official X developer app.
2. Request only the permissions needed for your own-account import.
3. Set credentials in `.env` (at minimum `X_API_BEARER_TOKEN` and `X_USER_ID`).
4. Respect published rate limits and API terms.

Import from API:

```bash
python -m src.main import-api --since 2025-01-01
```

## List Activity

```bash
python -m src.main list-activity --limit 100
```

## Export Data

JSON:

```bash
python -m src.main export-json --output ./data/exports/activity.json
```

CSV:

```bash
python -m src.main export-csv --output ./data/exports/activity.csv
```

## Generate Report

```bash
python -m src.main report --output ./data/reports/activity-summary.md
```

## Normalized Activity Schema

```json
{
  "id": "",
  "source": "x_archive | x_api",
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

## Database Tables

- `activities`
- `imports`
- `profiles`
- `raw_items`

## Security Notes

- Store API keys and tokens only in environment variables.
- `.gitignore` excludes `.env`, database files, and import/export/report data folders.
- Sensitive fields are redacted in logs.

## Legal and Privacy Limitations

You are responsible for complying with X terms, developer policies, local laws, and privacy obligations. Use this tool only with data you are authorized to access and process.

## Roadmap

- n8n workflow integration for compliant local automations
- AI summarization options with explicit user control
- Interactive dashboard for local analytics
- Cross-platform social telemetry integrations
