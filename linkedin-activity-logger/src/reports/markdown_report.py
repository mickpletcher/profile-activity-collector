from pathlib import Path

from profile_activity_core.database import Database
from profile_activity_core.reports import build_markdown_report as _build_markdown_report


ENGAGEMENT_TYPES = {"posts", "comments", "reactions", "shares", "articles"}


def build_markdown_report(database: Database, output_path: Path) -> Path:
    return _build_markdown_report(database, output_path, "LinkedIn Activity Summary", ENGAGEMENT_TYPES)
