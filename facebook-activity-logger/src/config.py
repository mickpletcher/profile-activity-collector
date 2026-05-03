from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv


SENSITIVE_KEYS = {"token", "access_token", "email", "phone", "password", "session"}


@dataclass(frozen=True)
class AppConfig:
    project_root: Path
    database_path: Path
    data_dir: Path
    facebook_access_token: str


def redact_sensitive_fields(payload: dict) -> dict:
    redacted = {}
    for key, value in payload.items():
        lowered = key.lower()
        if any(sensitive in lowered for sensitive in SENSITIVE_KEYS):
            redacted[key] = "***REDACTED***"
        else:
            redacted[key] = value
    return redacted


def load_config(project_root: Path | None = None) -> AppConfig:
    root = project_root or Path(__file__).resolve().parents[1]
    load_dotenv(root / ".env")

    database_raw = os.getenv("DATABASE_PATH", "./facebook_activity.db")
    database_path = Path(database_raw)
    if not database_path.is_absolute():
        database_path = (root / database_path).resolve()

    return AppConfig(
        project_root=root,
        database_path=database_path,
        data_dir=root / "data",
        facebook_access_token=os.getenv("FACEBOOK_ACCESS_TOKEN", "").strip(),
    )
