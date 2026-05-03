from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from profile_activity_core.models import Activity, normalize_activity_type


NORMALIZED_ACTIVITY_TYPES = {
    "tweets",
    "replies",
    "reposts",
    "quote_posts",
    "likes",
    "bookmarks",
    "follows",
    "followers",
    "blocks",
    "mutes",
    "lists",
    "dm_metadata",
    "login_security_events",
    "unknown",
}


__all__ = ["Activity", "NORMALIZED_ACTIVITY_TYPES", "normalize_activity_type"]
