from __future__ import annotations

from pathlib import Path

from src.database import Database
from src.importers.x_archive_importer import XArchiveImporter
from src.parsers.json_parser import parse_archive_file


FIXTURES = Path(__file__).parent / "fixtures" / "x-archive"


def test_parser_reads_x_js_wrappers() -> None:
    activities = parse_archive_file(FIXTURES / "data" / "tweets.js")

    assert len(activities) == 1
    activity = activities[0].activity
    assert activity.activity_type == "tweets"
    assert activity.body == "Shipping a local-first activity collector"
    assert activity.url == "https://x.com/i/web/status/1800000000000000001"
    assert activity.actor == "example_user"


def test_parser_reads_all_lists_in_json_archive_file() -> None:
    activities = parse_archive_file(FIXTURES / "data" / "multi-list.json")

    assert len(activities) == 2
    assert {activity.activity.body for activity in activities} == {
        "First item from first list",
        "Second item from second list",
    }


def test_importer_is_idempotent_for_x_fixture_archive(tmp_path: Path) -> None:
    db = Database(tmp_path / "activity.db")
    db.init_db()
    importer = XArchiveImporter(db)

    first = importer.import_from_path(FIXTURES)
    second = importer.import_from_path(FIXTURES)

    assert first["items_found"] == 4
    assert first["items_imported"] == 4
    assert second["items_found"] == 4
    assert second["items_imported"] == 0
    assert db.get_raw_item_count() == 4
