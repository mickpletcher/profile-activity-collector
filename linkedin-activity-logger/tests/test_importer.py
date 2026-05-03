import json
from pathlib import Path

from src.database import Database
from src.importers.linkedin_archive_importer import LinkedInArchiveImporter


def test_importer_imports_csv_and_json_archive(tmp_path: Path) -> None:
    export_dir = tmp_path / "linkedin-archive"
    export_dir.mkdir(parents=True, exist_ok=True)

    (export_dir / "posts.csv").write_text(
        "Date,Content,URL\n2024-05-01,My linkedin post,https://www.linkedin.com/feed/update/urn:li:activity:123\n",
        encoding="utf-8",
    )

    (export_dir / "comments.json").write_text(
        json.dumps([
            {
                "created_at": "2024-05-02T10:00:00Z",
                "text": "Great update",
                "url": "https://www.linkedin.com/feed/update/urn:li:activity:123",
            }
        ]),
        encoding="utf-8",
    )

    db = Database(tmp_path / "activity.db")
    db.init_db()

    importer = LinkedInArchiveImporter(db)
    result = importer.import_from_path(export_dir)

    assert result["items_found"] >= 2
    assert result["items_imported"] >= 2

    activities = db.list_activities(limit=10)
    assert len(activities) >= 2
