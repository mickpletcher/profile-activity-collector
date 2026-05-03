from __future__ import annotations

import argparse
import json
from pathlib import Path

from src.config import load_config
from src.database import Database
from src.importers.x_api_importer import XAPIImporter
from src.importers.x_archive_importer import XArchiveImporter
from src.reports.csv_export import export_csv
from src.reports.json_export import export_json
from src.reports.markdown_report import build_markdown_report


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Compliant X Activity Logger")
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("init-db", help="Initialize SQLite database")

    import_archive_parser = subparsers.add_parser(
        "import-archive", help="Import X data archive files"
    )
    import_archive_parser.add_argument("--path", required=True, help="Path to X archive directory")

    import_api_parser = subparsers.add_parser(
        "import-api", help="Import from official X API where permissions allow"
    )
    import_api_parser.add_argument("--since", required=True, help="Date in YYYY-MM-DD format")

    list_parser = subparsers.add_parser("list-activity", help="List normalized activities")
    list_parser.add_argument("--limit", type=int, default=100, help="Maximum records to list")

    export_json_parser = subparsers.add_parser("export-json", help="Export activities to JSON")
    export_json_parser.add_argument("--output", required=True, help="Output path for JSON")

    export_csv_parser = subparsers.add_parser("export-csv", help="Export activities to CSV")
    export_csv_parser.add_argument("--output", required=True, help="Output path for CSV")

    report_parser = subparsers.add_parser("report", help="Generate markdown activity report")
    report_parser.add_argument("--output", required=True, help="Output path for markdown report")

    return parser


def main() -> None:
    args = build_parser().parse_args()
    config = load_config()
    database = Database(config.database_path)

    if args.command == "init-db":
        database.init_db()
        print(f"Database initialized: {config.database_path}")
        return

    database.init_db()

    if args.command == "import-archive":
        importer = XArchiveImporter(database)
        result = importer.import_from_path(Path(args.path))
        print(json.dumps(result, indent=2))
        return

    if args.command == "import-api":
        importer = XAPIImporter(database, config.x_api_bearer_token, config.x_user_id)
        result = importer.import_since(args.since)
        print(json.dumps(result, indent=2))
        return

    if args.command == "list-activity":
        activities = database.list_activities(limit=args.limit)
        print(json.dumps([activity.to_dict() for activity in activities], indent=2, ensure_ascii=True))
        return

    if args.command == "export-json":
        output = export_json(database, Path(args.output))
        print(f"Exported JSON: {output}")
        return

    if args.command == "export-csv":
        output = export_csv(database, Path(args.output))
        print(f"Exported CSV: {output}")
        return

    if args.command == "report":
        output = build_markdown_report(database, Path(args.output))
        print(f"Generated report: {output}")
        return


if __name__ == "__main__":
    main()
