# LinkedIn Activity Logger (Compliant, Local-First)

This project is a compliant, local-first Python CLI for importing and analyzing your own LinkedIn account activity data from permitted sources.

## Privacy Warning

This tool processes potentially sensitive personal account data. Keep imported archives, database files, and generated reports local. Never commit personal data or credentials.

## What This Tool Does

- Imports your LinkedIn data archive exports (primary source).
- Supports optional official LinkedIn API import when valid permissions allow it.
- Normalizes activity into a consistent event schema.
- Stores normalized events and raw source records in local SQLite.
- Exports normalized activity to JSON and CSV.
- Generates a markdown summary report.

## What This Tool Does Not Do

- Does not bypass authentication, privacy controls, access restrictions, or rate limits.
- Does not evade bot detection or platform protections.
- Does not scrape private data from other users.
- Does not automate prohibited behavior.

## Supported Sources

1. LinkedIn data archive export files
2. Official LinkedIn API where valid permissions exist
3. Manual import folder for downloaded CSV or JSON files

## Project Structure

```text
linkedin-activity-logger/
  README.md
  requirements.txt
  .env.example
  src/
    main.py
    config.py
    database.py
    models.py
    importers/
      linkedin_archive_importer.py
      linkedin_api_importer.py
    parsers/
      csv_parser.py
      json_parser.py
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

If you plan to use API import, set `LINKEDIN_ACCESS_TOKEN` and `LINKEDIN_PERSON_URN` in `.env`.

## Initialize Database

```bash
python -m src.main init-db
```

## How To Download Your LinkedIn Data Archive Manually

1. Sign in to LinkedIn.
2. Open Settings and Privacy.
3. Go to Data Privacy and request "Download your data".
4. Select the data categories you want.
5. Download and extract the archive to a local folder, for example `./data/imports/linkedin-archive`.

## Import Archive Data

```bash
python -m src.main import-archive --path ./data/imports/linkedin-archive
```

## Configure Official LinkedIn API Access

1. Create and configure an official LinkedIn app.
2. Request only permissions required for your own account data.
3. Set credentials in `.env`.
4. Respect LinkedIn API terms and rate limits.

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
  "source": "linkedin_archive | linkedin_api",
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

- activities
- imports
- profiles
- raw_items

## Security Notes

- Store API keys and access tokens only in environment variables.
- `.gitignore` excludes `.env`, database files, and import/export/report folders.
- Sensitive fields are redacted in logs.

## Legal and Privacy Limitations

You are responsible for complying with LinkedIn terms, developer policies, local laws, and privacy obligations. Use this tool only with data you are authorized to access and process.

## Roadmap

- n8n integration for compliant local automations
- AI summarization options with explicit user control
- Dashboard support for local visual analytics
- Cross-platform social telemetry integrations
