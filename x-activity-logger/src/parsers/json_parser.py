from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from src.models import Activity, normalize_activity_type
from src.parsers.js_archive_parser import parse_js_archive_file


@dataclass
class ParsedActivity:
    activity: Activity
    raw_item: dict[str, Any]
    source_file: str


def infer_activity_type_from_path(path: Path) -> str:
    file_name = path.as_posix().lower()
    if "tweet" in file_name:
        return "tweets"
    if "reply" in file_name:
        return "replies"
    if "repost" in file_name or "retweet" in file_name:
        return "reposts"
    if "quote" in file_name:
        return "quote_posts"
    if "like" in file_name:
        return "likes"
    if "bookmark" in file_name:
        return "bookmarks"
    if "follow" in file_name and "follower" not in file_name:
        return "follows"
    if "follower" in file_name:
        return "followers"
    if "block" in file_name:
        return "blocks"
    if "mute" in file_name:
        return "mutes"
    if "list" in file_name:
        return "lists"
    if "direct_message" in file_name or "dm" in file_name:
        return "dm_metadata"
    if "login" in file_name or "security" in file_name or "account" in file_name:
        return "login_security_events"
    return "unknown"


def parse_archive_file(path: Path, source: str = "x_archive") -> list[ParsedActivity]:
    if path.suffix.lower() == ".js":
        content = parse_js_archive_file(path)
    else:
        with path.open("r", encoding="utf-8") as handle:
            content = json.load(handle)

    activity_type = infer_activity_type_from_path(path)
    items = _extract_items(content)

    parsed: list[ParsedActivity] = []
    for item in items:
        normalized_item = _unwrap_common_wrappers(item)

        created_at = _extract_created_at(normalized_item)
        body = _extract_body(normalized_item)
        title = _extract_title(normalized_item, activity_type, body)
        url = _extract_url(normalized_item)
        actor = _extract_actor(normalized_item)
        target = _extract_target(normalized_item)

        if not any([created_at, body, title, url]):
            continue

        metadata = {
            "source_file": path.as_posix(),
            "parser": "json_parser",
            "raw_keys": sorted(list(normalized_item.keys())),
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
                raw_item=normalized_item,
                source_file=path.as_posix(),
            )
        )

    return parsed


def _extract_items(content: Any) -> list[dict[str, Any]]:
    if isinstance(content, list):
        return [item for item in content if isinstance(item, dict)]

    if isinstance(content, dict):
        for value in content.values():
            if isinstance(value, list):
                return [item for item in value if isinstance(item, dict)]
        return [content]

    return []


def _unwrap_common_wrappers(item: dict[str, Any]) -> dict[str, Any]:
    for key in ("tweet", "like", "follower", "following", "block", "mute", "dmConversation"):
        nested = item.get(key)
        if isinstance(nested, dict):
            merged = dict(nested)
            merged.setdefault("_wrapper", key)
            return merged
    return item


def _extract_created_at(item: dict[str, Any]) -> str:
    for key in ("created_at", "createdAt", "timestamp"):
        value = item.get(key)
        if isinstance(value, str):
            return value
    return ""


def _extract_body(item: dict[str, Any]) -> str:
    for key in ("full_text", "text", "description", "message"):
        value = item.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()
    return ""


def _extract_title(item: dict[str, Any], activity_type: str, body: str) -> str:
    if isinstance(item.get("title"), str):
        return item["title"].strip()
    if body:
        return body[:100]
    return activity_type.replace("_", " ").title()


def _extract_url(item: dict[str, Any]) -> str:
    if isinstance(item.get("expanded_url"), str):
        return item["expanded_url"]

    if isinstance(item.get("id_str"), str):
        return f"https://x.com/i/web/status/{item['id_str']}"

    if isinstance(item.get("tweet_id"), str):
        return f"https://x.com/i/web/status/{item['tweet_id']}"

    return ""


def _extract_actor(item: dict[str, Any]) -> str:
    for key in ("screen_name", "name", "sender_id"):
        value = item.get(key)
        if isinstance(value, str):
            return value
    return ""


def _extract_target(item: dict[str, Any]) -> str:
    for key in ("in_reply_to_screen_name", "recipient_id", "list_name"):
        value = item.get(key)
        if isinstance(value, str):
            return value
    return ""
