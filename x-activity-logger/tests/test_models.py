from src.models import Activity, normalize_activity_type


def test_normalize_activity_type_unknown() -> None:
    assert normalize_activity_type("not_real") == "unknown"


def test_activity_to_db_record() -> None:
    activity = Activity(
        id="abc",
        source="x_archive",
        activity_type="tweets",
        title="Hello",
        body="Body",
        url="",
        created_at="2026-01-01T00:00:00Z",
        updated_at="2026-01-01T00:00:00Z",
        actor="me",
        target="",
        metadata={"k": "v"},
    )

    record = activity.to_db_record()
    assert record[0] == "abc"
    assert record[2] == "tweets"
