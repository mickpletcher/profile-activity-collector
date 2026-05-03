from __future__ import annotations

from src.database import Database


def build_activity_summary(database: Database) -> dict:
    counts = database.get_activity_counts()
    total = sum(counts.values())
    return {
        "total_activities": total,
        "counts_by_type": counts,
    }
