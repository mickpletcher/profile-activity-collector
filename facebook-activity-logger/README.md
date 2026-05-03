# Facebook Activity Logger (Compliant, Local-First)

This project is a compliant, local-first Python CLI for importing and analyzing your own Facebook profile activity data from permitted data sources.

## Privacy Warning

This tool processes potentially sensitive personal data. Keep all imported files and generated outputs local. Never commit personal exports, database files, access tokens, or reports containing private data.

## What This Tool Does

- Imports your Facebook Download Your Information (DYI) export files (JSON-first).
- Supports optional Meta Graph API import only where your app/user permissions legally allow it.
- Normalizes activity into a consistent event schema.
- Stores normalized events and raw source items in local SQLite.
- Exports normalized data to JSON and CSV.
- Generates a markdown summary report.

## What This Tool Does Not Do

- Does not bypass authentication, privacy controls, or access restrictions.
- Does not evade bot detection or rate limits.
- Does not scrape private data from other users.
- Does not automate prohibited behavior on Facebook properties.

## Supported Sources

1. Facebook Download Your Information export files (primary source)
2. Meta Graph API where valid user permissions exist
3. Manual import folder for downloaded JSON/HTML files

## Project Structure

```text
facebook-activity-logger/
  README.md
  requirements.txt
  .env.example
  src/
    main.py
    config.py
    database.py
    models.py
    importers/
      facebook_export_importer.py
      graph_api_importer.py
    parsers/
      json_parser.py
      html_parser.py
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

If you plan to use Graph API import, set `FACEBOOK_ACCESS_TOKEN` in `.env`.

## Initialize Database

```bash
python -m src.main init-db
```

## How To Download Facebook Data Manually

1. Go to Facebook Settings.
2. Open "Your Facebook Information".
3. Select "Download Your Information".
4. Choose JSON format when possible.
5. Select the activity categories you want (posts, comments, reactions, etc.).
6. Download and extract the archive to a local folder.

## Import Data

Import a local Facebook export folder:

```bash
python -m src.main import-export --path ./data/imports/facebook-export
```

Import from Graph API (only if you have valid permissions):

```bash
python -m src.main import-graph --since 2025-01-01
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
  "source": "facebook_export | graph_api",
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

- Keep access tokens only in environment variables.
- `.gitignore` excludes `.env`, local databases, and import/export/report data folders.
- Logging utilities redact sensitive fields.

## Legal and Privacy Limitations

You are responsible for complying with Facebook and Meta Terms, applicable laws, and privacy obligations. Use this tool only with data you are authorized to access and process.

## Roadmap

- n8n workflow integration for compliant local automation
- AI summarization pipeline (local or user-approved provider)
- Lightweight dashboard for visual analytics
- Expanded parser support for additional export file layouts
