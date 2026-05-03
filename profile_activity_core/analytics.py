from __future__ import annotations

from profile_activity_core.database import Database


def build_activity_summary(database: Database) -> dict:
    counts = database.get_activity_counts()
    total = sum(counts.values())
    return {
        "total_activities": total,
        "counts_by_type": counts,
    }


def build_engagement_summary(database: Database, engagement_types: set[str]) -> dict:
    counts = database.get_activity_counts()
    engagement_total = sum(value for key, value in counts.items() if key in engagement_types)
    return {
        "engagement_total": engagement_total,
        "engagement_breakdown": {key: value for key, value in counts.items() if key in engagement_types},
    }
