from __future__ import annotations

from pathlib import Path

import pytest

from profile_activity_core.database import Database
from profile_activity_core.models import Activity
from profile_activity_core.validation import ValidationError


def make_activity(activity_id: str = "1") -> Activity:
    return Activity(
        id=activity_id,
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


def test_database_dedupes_raw_items(tmp_path: Path) -> None:
    db = Database(tmp_path / "activity.db")
    db.init_db()
    activity = make_activity()

    assert db.insert_activity(activity) is True
    assert db.insert_raw_item("x_archive", "tweets.js", activity.id, {"id": "1"}) is True
    assert db.insert_raw_item("x_archive", "tweets.js", activity.id, {"id": "1"}) is False
    assert db.get_raw_item_count() == 1


def test_database_rejects_invalid_activity(tmp_path: Path) -> None:
    db = Database(tmp_path / "activity.db")
    db.init_db()
    activity = make_activity(activity_id="")

    with pytest.raises(ValidationError):
        db.insert_activity(activity)


def test_database_rejects_unsupported_activity_type(tmp_path: Path) -> None:
    db = Database(tmp_path / "activity.db")
    db.init_db()
    activity = make_activity()
    activity.activity_type = "not_real"

    with pytest.raises(ValidationError):
        db.insert_activity(activity)
