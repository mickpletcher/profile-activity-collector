from pathlib import Path

from src.database import Database
from src.importers.x_archive_importer import XArchiveImporter


def test_importer_imports_js_archive(tmp_path: Path) -> None:
    export_dir = tmp_path / "x-archive"
    export_dir.mkdir(parents=True, exist_ok=True)

    tweets_js = "window.YTD.tweets.part0 = [{\"tweet\": {\"id_str\": \"123\", \"full_text\": \"hello x\", \"created_at\": \"2024-01-01T00:00:00Z\"}}];"
    (export_dir / "tweets.js").write_text(tweets_js, encoding="utf-8")

    db = Database(tmp_path / "activity.db")
    db.init_db()

    importer = XArchiveImporter(db)
    result = importer.import_from_path(export_dir)

    assert result["items_found"] >= 1
    assert result["items_imported"] >= 1

    activities = db.list_activities(limit=5)
    assert activities
    assert activities[0].activity_type in {"tweets", "unknown"}
