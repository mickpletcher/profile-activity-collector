from __future__ import annotations

from pathlib import Path

from src.parsers.json_parser import ParsedActivity


def parse_html_file(path: Path) -> list[ParsedActivity]:
    """Placeholder parser for optional Facebook HTML exports.

    HTML parsing is intentionally minimal in the first implementation.
    JSON export ingestion is the primary, recommended ingestion path.
    """
    _ = path
    return []
