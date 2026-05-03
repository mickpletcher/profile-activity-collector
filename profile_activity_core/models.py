from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from hashlib import sha256
from typing import Any


NORMALIZED_ACTIVITY_TYPES = {
    "articles",
    "blocks",
    "bookmarks",
    "comments",
    "companies_followed",
    "connections",
    "dm_metadata",
    "follows",
    "followers",
    "friend_activity",
    "groups",
    "groups_activity",
    "likes",
    "lists",
    "login_security_events",
    "messages_metadata",
    "mutes",
    "pages_activity",
    "posts",
    "profile_changes",
    "quote_posts",
    "reactions",
    "replies",
    "reposts",
    "search_history",
    "shares",
    "tweets",
    "unknown",
}


def normalize_activity_type(activity_type: str) -> str:
    normalized = activity_type.strip().lower().replace(" ", "_")
    if normalized not in NORMALIZED_ACTIVITY_TYPES:
        return "unknown"
    return normalized


@dataclass
class Activity:
    id: str
    source: str
    activity_type: str
    title: str
    body: str
    url: str
    created_at: str
    updated_at: str
    actor: str
    target: str
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_db_record(self) -> tuple:
        return (
            self.id,
            self.source,
            normalize_activity_type(self.activity_type),
            self.title,
            self.body,
            self.url,
            self.created_at,
            self.updated_at,
            self.actor,
            self.target,
            json.dumps(self.metadata, ensure_ascii=True),
        )

    @classmethod
    def from_db_row(cls, row: dict[str, Any]) -> "Activity":
        metadata_raw = row.get("metadata") or "{}"
        metadata = json.loads(metadata_raw)
        return cls(
            id=row["id"],
            source=row["source"],
            activity_type=row["activity_type"],
            title=row.get("title") or "",
            body=row.get("body") or "",
            url=row.get("url") or "",
            created_at=row.get("created_at") or "",
            updated_at=row.get("updated_at") or "",
            actor=row.get("actor") or "",
            target=row.get("target") or "",
            metadata=metadata,
        )

    @classmethod
    def build_id(
        cls,
        source: str,
        activity_type: str,
        created_at: str,
        title: str,
        body: str,
        source_file: str,
        source_item_id: str = "",
    ) -> str:
        identity_parts = [
            source,
            normalize_activity_type(activity_type),
            source_item_id,
            created_at,
            title,
            body,
        ]
        if not source_item_id:
            identity_parts.append(source_file)
        identity = "|".join(identity_parts)
        return sha256(identity.encode("utf-8")).hexdigest()

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
