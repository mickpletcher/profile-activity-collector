from __future__ import annotations

import json
from pathlib import Path

from src.database import Database


def export_json(database: Database, output_path: Path) -> Path:
    activities = [activity.to_dict() for activity in database.get_all_activities()]
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(activities, indent=2, ensure_ascii=True), encoding="utf-8")
    return output_path
