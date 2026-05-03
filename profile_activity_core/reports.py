from __future__ import annotations

import csv
import json
from datetime import datetime, timezone
from pathlib import Path

from profile_activity_core.analytics import build_activity_summary, build_engagement_summary
from profile_activity_core.database import Database


CSV_COLUMNS = [
    "id",
    "source",
    "activity_type",
    "title",
    "body",
    "url",
    "created_at",
    "updated_at",
    "actor",
    "target",
]


def export_csv(database: Database, output_path: Path) -> Path:
    activities = database.get_all_activities()
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with output_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=CSV_COLUMNS)
        writer.writeheader()
        for activity in activities:
            row = activity.to_dict()
            writer.writerow({column: row.get(column, "") for column in CSV_COLUMNS})

    return output_path


def export_json(database: Database, output_path: Path) -> Path:
    activities = [activity.to_dict() for activity in database.get_all_activities()]
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(activities, indent=2, ensure_ascii=True), encoding="utf-8")
    return output_path


def build_markdown_report(
    database: Database,
    output_path: Path,
    title: str,
    engagement_types: set[str],
) -> Path:
    summary = build_activity_summary(database)
    engagement = build_engagement_summary(database, engagement_types)
    latest = database.list_activities(limit=10)

    lines: list[str] = []
    lines.append(f"# {title}")
    lines.append("")
    lines.append(f"Generated at: {datetime.now(timezone.utc).isoformat()}")
    lines.append("")
    lines.append("## Totals")
    lines.append("")
    lines.append(f"- Total activities: {summary['total_activities']}")
    lines.append(f"- Engagement total: {engagement['engagement_total']}")
    lines.append("")
    lines.append("## Counts By Type")
    lines.append("")

    if summary["counts_by_type"]:
        for activity_type, count in summary["counts_by_type"].items():
            lines.append(f"- {activity_type}: {count}")
    else:
        lines.append("- No activities found.")

    lines.append("")
    lines.append("## Recent Activity")
    lines.append("")

    if latest:
        for activity in latest:
            lines.append(
                f"- {activity.created_at or 'unknown-date'} | {activity.activity_type} | {activity.title or '(no title)'}"
            )
    else:
        lines.append("- No recent activity available.")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return output_path
