from __future__ import annotations

import csv
from pathlib import Path

from src.database import Database


CSV_COLUMNS = [
    "id",
    "source",
    "activity_type",
    "title",
    "body",
    "url",
    "created_at",
    "updated_at",
    "actor",
    "target",
]


def export_csv(database: Database, output_path: Path) -> Path:
    activities = database.get_all_activities()
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with output_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=CSV_COLUMNS)
        writer.writeheader()
        for activity in activities:
            row = activity.to_dict()
            writer.writerow({column: row.get(column, "") for column in CSV_COLUMNS})

    return output_path
