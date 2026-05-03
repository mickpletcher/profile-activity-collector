from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv


SENSITIVE_KEYS = {
    "token",
    "access_token",
    "secret",
    "api_key",
    "bearer",
    "email",
    "phone",
    "password",
    "session",
}


@dataclass(frozen=True)
class AppConfig:
    project_root: Path
    database_path: Path
    data_dir: Path
    x_api_bearer_token: str
    x_user_id: str


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

    database_raw = os.getenv("DATABASE_PATH", "./x_activity.db")
    database_path = Path(database_raw)
    if not database_path.is_absolute():
        database_path = (root / database_path).resolve()

    return AppConfig(
        project_root=root,
        database_path=database_path,
        data_dir=root / "data",
        x_api_bearer_token=os.getenv("X_API_BEARER_TOKEN", "").strip(),
        x_user_id=os.getenv("X_USER_ID", "").strip(),
    )
