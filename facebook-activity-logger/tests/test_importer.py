import json
from pathlib import Path

from src.database import Database
from src.importers.facebook_export_importer import FacebookExportImporter


def test_importer_imports_json_export(tmp_path: Path) -> None:
    export_dir = tmp_path / "facebook-export"
    export_dir.mkdir(parents=True, exist_ok=True)

    sample = {
        "comments_v2": [
            {
                "timestamp": 1715000000,
                "title": "Commented on a post",
                "data": [{"comment": "Nice work!"}],
            }
        ]
    }
    (export_dir / "comments.json").write_text(json.dumps(sample), encoding="utf-8")

    db = Database(tmp_path / "activity.db")
    db.init_db()

    importer = FacebookExportImporter(db)
    result = importer.import_from_path(export_dir)

    assert result["items_found"] >= 1
    assert result["items_imported"] >= 1

    activities = db.list_activities(limit=5)
    assert activities
    assert activities[0].activity_type in {"comments", "unknown"}
