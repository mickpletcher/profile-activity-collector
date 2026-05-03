from __future__ import annotations

from pathlib import Path

from src.database import Database
from src.importers.facebook_export_importer import FacebookExportImporter
from src.parsers.json_parser import parse_json_file


FIXTURES = Path(__file__).parent / "fixtures" / "facebook-export"


def test_parser_reads_facebook_comment_export() -> None:
    activities = parse_json_file(FIXTURES / "comments.json")

    assert len(activities) >= 1
    comment = next(activity.activity for activity in activities if activity.activity.activity_type == "comments")
    assert comment.body == "Nice work on the launch."
    assert comment.title == "Guy commented on a post"
    assert comment.url == "https://www.facebook.com/example/posts/100"
    assert comment.created_at == "2024-05-06T12:53:20+00:00"


def test_importer_is_idempotent_for_facebook_fixture_export(tmp_path: Path) -> None:
    db = Database(tmp_path / "activity.db")
    db.init_db()
    importer = FacebookExportImporter(db)

    first = importer.import_from_path(FIXTURES)
    second = importer.import_from_path(FIXTURES)

    assert first["items_found"] >= 2
    assert first["items_imported"] >= 2
    assert second["items_found"] == first["items_found"]
    assert second["items_imported"] == 0
    assert db.get_raw_item_count() == first["items_found"]
