from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from src.models import Activity, normalize_activity_type


TIMESTAMP_KEYS = ("timestamp", "creation_timestamp", "created_timestamp", "start_timestamp")


@dataclass
class ParsedActivity:
    activity: Activity
    raw_item: dict[str, Any]
    source_file: str


def infer_activity_type_from_path(path: Path) -> str:
    file_name = path.as_posix().lower()
    if "comment" in file_name:
        return "comments"
    if "reaction" in file_name:
        return "reactions"
    if "like" in file_name:
        return "likes"
    if "share" in file_name:
        return "shares"
    if "profile" in file_name:
        return "profile_changes"
    if "friend" in file_name:
        return "friend_activity"
    if "group" in file_name:
        return "groups_activity"
    if "page" in file_name:
        return "pages_activity"
    if "message" in file_name:
        return "messages_metadata"
    if "security" in file_name or "login" in file_name:
        return "login_security_events"
    if "post" in file_name or "timeline" in file_name:
        return "posts"
    return "unknown"


def parse_json_file(path: Path, source: str = "facebook_export") -> list[ParsedActivity]:
    with path.open("r", encoding="utf-8") as handle:
        content = json.load(handle)

    activity_type = infer_activity_type_from_path(path)
    candidates = _extract_candidates(content)
    parsed: list[ParsedActivity] = []

    for candidate in candidates:
        created_at = _extract_created_at(candidate)
        title = _extract_title(candidate)
        body = _extract_body(candidate)
        url = _extract_url(candidate)
        actor = _extract_actor(candidate)
        target = _extract_target(candidate)

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

        parsed.append(
            ParsedActivity(
                activity=activity,
                raw_item=candidate,
                source_file=path.as_posix(),
            )
        )

    return parsed


def _extract_candidates(node: Any) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []

    def walk(value: Any) -> None:
        if isinstance(value, dict):
            has_timestamp = any(key in value for key in TIMESTAMP_KEYS)
            has_textual_content = any(
                key in value for key in ("title", "data", "post", "comment", "text", "url", "attachments")
            )
            if has_timestamp or has_textual_content:
                results.append(value)

            for nested in value.values():
                walk(nested)
        elif isinstance(value, list):
            for nested in value:
                walk(nested)

    walk(node)

    unique_results: list[dict[str, Any]] = []
    seen = set()
    for item in results:
        signature = json.dumps(item, sort_keys=True, ensure_ascii=True, default=str)
        if signature not in seen:
            seen.add(signature)
            unique_results.append(item)

    return unique_results


def _extract_created_at(item: dict[str, Any]) -> str:
    for key in TIMESTAMP_KEYS:
        if key not in item:
            continue
        value = item.get(key)
        if isinstance(value, (int, float)):
            return datetime.fromtimestamp(value, tz=timezone.utc).isoformat()
        if isinstance(value, str):
            return value
    return ""


def _extract_title(item: dict[str, Any]) -> str:
    if isinstance(item.get("title"), str):
        return item["title"].strip()
    body = _extract_body(item)
    if body:
        return body[:100]
    return ""


def _extract_body(item: dict[str, Any]) -> str:
    for key in ("post", "comment", "text", "message", "description"):
        value = item.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()

    data = item.get("data")
    if isinstance(data, list):
        parts: list[str] = []
        for piece in data:
            if not isinstance(piece, dict):
                continue
            for key in ("post", "comment", "reaction", "update", "text"):
                value = piece.get(key)
                if isinstance(value, str) and value.strip():
                    parts.append(value.strip())
        if parts:
            return " | ".join(parts)

    return ""


def _extract_url(item: dict[str, Any]) -> str:
    for key in ("url", "href", "permalink"):
        value = item.get(key)
        if isinstance(value, str):
            return value

    attachments = item.get("attachments")
    if isinstance(attachments, list):
        for attachment in attachments:
            if not isinstance(attachment, dict):
                continue
            if isinstance(attachment.get("url"), str):
                return attachment["url"]

    return ""


def _extract_actor(item: dict[str, Any]) -> str:
    for key in ("author", "name", "sender_name"):
        value = item.get(key)
        if isinstance(value, str):
            return value
    return ""


def _extract_target(item: dict[str, Any]) -> str:
    for key in ("group", "page", "target"):
        value = item.get(key)
        if isinstance(value, str):
            return value
    return ""
