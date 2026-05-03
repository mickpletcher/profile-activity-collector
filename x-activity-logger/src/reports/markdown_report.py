from pathlib import Path

from profile_activity_core.database import Database
from profile_activity_core.reports import build_markdown_report as _build_markdown_report


ENGAGEMENT_TYPES = {"tweets", "replies", "reposts", "quote_posts", "likes"}


def build_markdown_report(database: Database, output_path: Path) -> Path:
    return _build_markdown_report(database, output_path, "X Activity Summary", ENGAGEMENT_TYPES)
