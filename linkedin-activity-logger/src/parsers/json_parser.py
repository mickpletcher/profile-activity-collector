from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from src.models import Activity, normalize_activity_type


@dataclass
class ParsedActivity:
    activity: Activity
    raw_item: dict[str, Any]
    source_file: str


def infer_activity_type_from_path(path: Path) -> str:
    file_name = path.name.lower()
    if "comment" in file_name:
        return "comments"
    if "reaction" in file_name or "like" in file_name:
        return "reactions"
    if "share" in file_name:
        return "shares"
    if "article" in file_name:
        return "articles"
    if "profile" in file_name:
        return "profile_changes"
    if "connection" in file_name:
        return "connections"
    if "follower" in file_name:
        return "followers"
    if "company" in file_name:
        return "companies_followed"
    if "group" in file_name:
        return "groups"
    if "message" in file_name:
        return "messages_metadata"
    if "search" in file_name:
        return "search_history"
    if "security" in file_name or "login" in file_name:
        return "login_security_events"
    if "post" in file_name or "update" in file_name:
        return "posts"
    return "unknown"


def parse_json_file(path: Path, source: str = "linkedin_archive") -> list[ParsedActivity]:
    with path.open("r", encoding="utf-8") as handle:
        content = json.load(handle)

    activity_type = infer_activity_type_from_path(path)
    candidates = _extract_candidates(content)

    parsed: list[ParsedActivity] = []
    for candidate in candidates:
        created_at = _pick(candidate, ["created_at", "timestamp", "date", "time"])
        body = _pick(candidate, ["content", "text", "message", "body", "description"])
        title = _pick(candidate, ["title", "subject", "type"]) or (body[:100] if body else activity_type)
        url = _pick(candidate, ["url", "link", "permalink"])
        actor = _pick(candidate, ["actor", "name", "author", "from"])
        target = _pick(candidate, ["target", "to", "company", "group"])
        source_item_id = _pick(candidate, ["id", "urn", "entityUrn", "post_id"])

        if not any([created_at, title, body, url]):
            continue

        metadata = {
            "source_file": path.as_posix(),
            "parser": "json_parser",
            "raw_keys": sorted(list(candidate.keys())),
        }

        activity = Activity(
            id=Activity.build_id(
                source=source,
                activity_type=activity_type,
                created_at=created_at,
                title=title,
                body=body,
                source_file=path.as_posix(),
                source_item_id=source_item_id,
            ),
            source=source,
            activity_type=normalize_activity_type(activity_type),
            title=title,
            body=body,
            url=url,
            created_at=created_at,
            updated_at=created_at,
            actor=actor,
            target=target,
            metadata=metadata,
        )

        parsed.append(ParsedActivity(activity=activity, raw_item=candidate, source_file=path.as_posix()))

    return parsed


def _extract_candidates(node: Any) -> list[dict[str, Any]]:
    if isinstance(node, list):
        return [item for item in node if isinstance(item, dict)]

    if isinstance(node, dict):
        list_values: list[dict[str, Any]] = []
        for value in node.values():
            if isinstance(value, list):
                list_values.extend(item for item in value if isinstance(item, dict))
        return list_values or [node]

    return []


def _pick(item: dict[str, Any], keys: list[str]) -> str:
    for key in keys:
        value = item.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()
    return ""
