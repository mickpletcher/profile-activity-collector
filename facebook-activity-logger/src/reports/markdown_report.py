from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

from src.analytics.activity_summary import build_activity_summary
from src.analytics.engagement_summary import build_engagement_summary
from src.database import Database


def build_markdown_report(database: Database, output_path: Path) -> Path:
    summary = build_activity_summary(database)
    engagement = build_engagement_summary(database)
    latest = database.list_activities(limit=10)

    lines: list[str] = []
    lines.append("# Facebook Activity Summary")
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
