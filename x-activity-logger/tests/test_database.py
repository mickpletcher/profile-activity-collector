from pathlib import Path

from src.database import Database
from src.models import Activity


def test_database_init_and_insert(tmp_path: Path) -> None:
    db = Database(tmp_path / "test.db")
    db.init_db()

    activity = Activity(
        id="1",
        source="x_archive",
        activity_type="tweets",
        title="Tweet",
        body="Test body",
        url="",
        created_at="2026-01-01T00:00:00Z",
        updated_at="2026-01-01T00:00:00Z",
        actor="me",
        target="",
        metadata={},
    )

    assert db.insert_activity(activity) is True
    assert db.insert_activity(activity) is False

    items = db.list_activities(limit=10)
    assert len(items) == 1
    assert items[0].id == "1"
