from __future__ import annotations

from pathlib import Path

from src.database import Database
from src.importers.linkedin_archive_importer import LinkedInArchiveImporter
from src.parsers.csv_parser import parse_csv_file
from src.parsers.json_parser import parse_json_file


FIXTURES = Path(__file__).parent / "fixtures" / "linkedin-archive"


def test_parser_reads_linkedin_csv_post_export() -> None:
    activities = parse_csv_file(FIXTURES / "posts.csv")

    assert len(activities) == 1
    activity = activities[0].activity
    assert activity.activity_type == "posts"
    assert activity.body == "My linkedin post"
    assert activity.actor == "Guy"
    assert activity.url == "https://www.linkedin.com/feed/update/urn:li:activity:123"


def test_parser_reads_linkedin_json_comment_export() -> None:
    activities = parse_json_file(FIXTURES / "Comments.json")

    assert len(activities) == 1
    activity = activities[0].activity
    assert activity.activity_type == "comments"
    assert activity.body == "Great update"
    assert activity.actor == "Guy"


def test_importer_is_idempotent_for_linkedin_fixture_archive(tmp_path: Path) -> None:
    db = Database(tmp_path / "activity.db")
    db.init_db()
    importer = LinkedInArchiveImporter(db)

    first = importer.import_from_path(FIXTURES)
    second = importer.import_from_path(FIXTURES)

    assert first["items_found"] == 3
    assert first["items_imported"] == 3
    assert second["items_found"] == 3
    assert second["items_imported"] == 0
    assert db.get_raw_item_count() == 3
