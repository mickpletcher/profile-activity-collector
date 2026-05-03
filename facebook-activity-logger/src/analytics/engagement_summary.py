from __future__ import annotations

from src.database import Database


ENGAGEMENT_TYPES = {"posts", "comments", "reactions", "likes", "shares"}


def build_engagement_summary(database: Database) -> dict:
    counts = database.get_activity_counts()
    engagement_total = sum(value for key, value in counts.items() if key in ENGAGEMENT_TYPES)
    return {
        "engagement_total": engagement_total,
        "engagement_breakdown": {key: value for key, value in counts.items() if key in ENGAGEMENT_TYPES},
    }
