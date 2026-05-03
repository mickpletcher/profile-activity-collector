from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from profile_activity_core.models import Activity, NORMALIZED_ACTIVITY_TYPES


@dataclass(frozen=True)
class ValidationIssue:
    field: str
    message: str


class ValidationError(ValueError):
    def __init__(self, issues: list[ValidationIssue]) -> None:
        self.issues = issues
        message = "; ".join(f"{issue.field}: {issue.message}" for issue in issues)
        super().__init__(message)


def validate_activity(activity: Activity) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []

    if not activity.id.strip():
        issues.append(ValidationIssue("id", "activity id is required"))
    if not activity.source.strip():
        issues.append(ValidationIssue("source", "source is required"))

    normalized_type = activity.activity_type.strip().lower().replace(" ", "_")
    if normalized_type not in NORMALIZED_ACTIVITY_TYPES:
        issues.append(ValidationIssue("activity_type", "activity type is unsupported"))

    if not any([activity.created_at.strip(), activity.title.strip(), activity.body.strip(), activity.url.strip()]):
        issues.append(
            ValidationIssue(
                "activity",
                "at least one of created_at, title, body, or url is required",
            )
        )

    if activity.created_at and not _looks_like_datetime(activity.created_at):
        issues.append(ValidationIssue("created_at", "timestamp should be ISO-like or platform-native text"))

    return issues


def require_valid_activity(activity: Activity) -> None:
    issues = validate_activity(activity)
    if issues:
        raise ValidationError(issues)


def _looks_like_datetime(value: str) -> bool:
    stripped = value.strip()
    if not stripped:
        return True
    try:
        datetime.fromisoformat(stripped.replace("Z", "+00:00"))
        return True
    except ValueError:
        pass

    # Some platform archives use native strings such as "Wed Oct 10 20:19:24 +0000 2018".
    return any(char.isdigit() for char in stripped) and len(stripped) >= 8
