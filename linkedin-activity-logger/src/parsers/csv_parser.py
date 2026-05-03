from __future__ import annotations

import csv
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


def parse_csv_file(path: Path, source: str = "linkedin_archive") -> list[ParsedActivity]:
    activity_type = infer_activity_type_from_path(path)
    parsed: list[ParsedActivity] = []

    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            clean_row = {str(key): (value or "") for key, value in row.items() if key}
            created_at = _pick(clean_row, ["Date", "Timestamp", "Created At", "created_at", "time"])
            body = _pick(clean_row, ["Content", "Message", "Text", "Body", "Description", "comment"])
            title = _pick(clean_row, ["Title", "Subject", "Type"]) or (body[:100] if body else activity_type)
            url = _pick(clean_row, ["URL", "Link", "Permalink", "Post Link"])
            actor = _pick(clean_row, ["Actor", "Profile Name", "Name", "From"])
            target = _pick(clean_row, ["Target", "To", "Company", "Group"])
            source_item_id = _pick(clean_row, ["ID", "Id", "URN", "Entity URN", "Post ID"])

            if not any([created_at, title, body, url]):
                continue

            metadata = {
                "source_file": path.as_posix(),
                "parser": "csv_parser",
                "raw_keys": sorted(list(clean_row.keys())),
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

            parsed.append(ParsedActivity(activity=activity, raw_item=clean_row, source_file=path.as_posix()))

    return parsed


def _pick(row: dict[str, str], keys: list[str]) -> str:
    for key in keys:
        value = row.get(key, "")
        if value and value.strip():
            return value.strip()
    return ""
