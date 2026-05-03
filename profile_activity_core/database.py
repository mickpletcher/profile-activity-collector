from __future__ import annotations

import json
import sqlite3
from contextlib import contextmanager
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
from typing import Iterator

from profile_activity_core.models import Activity
from profile_activity_core.validation import require_valid_activity


class Database:
    def __init__(self, db_path: Path, strict_validation: bool = True) -> None:
        self.db_path = db_path
        self.strict_validation = strict_validation
        self.db_path.parent.mkdir(parents=True, exist_ok=True)

    @contextmanager
    def connection(self) -> Iterator[sqlite3.Connection]:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        finally:
            conn.close()

    def init_db(self) -> None:
        with self.connection() as conn:
            conn.executescript(
                """
                CREATE TABLE IF NOT EXISTS activities (
                    id TEXT PRIMARY KEY,
                    source TEXT NOT NULL,
                    activity_type TEXT NOT NULL,
                    title TEXT,
                    body TEXT,
                    url TEXT,
                    created_at TEXT,
                    updated_at TEXT,
                    actor TEXT,
                    target TEXT,
                    metadata TEXT NOT NULL DEFAULT '{}'
                );

                CREATE INDEX IF NOT EXISTS idx_activities_type ON activities(activity_type);
                CREATE INDEX IF NOT EXISTS idx_activities_created_at ON activities(created_at);
                CREATE INDEX IF NOT EXISTS idx_activities_source ON activities(source);

                CREATE TABLE IF NOT EXISTS imports (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    source TEXT NOT NULL,
                    import_path TEXT NOT NULL,
                    started_at TEXT NOT NULL,
                    finished_at TEXT,
                    status TEXT NOT NULL,
                    items_found INTEGER NOT NULL DEFAULT 0,
                    items_imported INTEGER NOT NULL DEFAULT 0,
                    error TEXT
                );

                CREATE TABLE IF NOT EXISTS profiles (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    profile_id TEXT UNIQUE,
                    profile_name TEXT,
                    metadata TEXT NOT NULL DEFAULT '{}',
                    updated_at TEXT NOT NULL
                );

                CREATE TABLE IF NOT EXISTS raw_items (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    source TEXT NOT NULL,
                    source_file TEXT NOT NULL,
                    activity_id TEXT,
                    raw_json TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    FOREIGN KEY(activity_id) REFERENCES activities(id)
                );

                CREATE INDEX IF NOT EXISTS idx_raw_items_activity ON raw_items(activity_id);
                """
            )
            self._ensure_raw_hash(conn)

    def insert_activity(self, activity: Activity) -> bool:
        if self.strict_validation:
            require_valid_activity(activity)

        with self.connection() as conn:
            cursor = conn.execute(
                """
                INSERT OR IGNORE INTO activities (
                    id, source, activity_type, title, body, url, created_at,
                    updated_at, actor, target, metadata
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                activity.to_db_record(),
            )
            return cursor.rowcount > 0

    def insert_raw_item(self, source: str, source_file: str, activity_id: str, raw_item: dict) -> bool:
        raw_json = json.dumps(raw_item, ensure_ascii=True, sort_keys=True, default=str)
        raw_hash = build_raw_item_hash(source, source_file, raw_json)
        with self.connection() as conn:
            cursor = conn.execute(
                """
                INSERT OR IGNORE INTO raw_items (
                    source, source_file, activity_id, raw_json, raw_hash, created_at
                ) VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    source,
                    source_file,
                    activity_id,
                    raw_json,
                    raw_hash,
                    datetime.now(timezone.utc).isoformat(),
                ),
            )
            return cursor.rowcount > 0

    def start_import(self, source: str, import_path: str) -> int:
        with self.connection() as conn:
            cursor = conn.execute(
                """
                INSERT INTO imports (source, import_path, started_at, status)
                VALUES (?, ?, ?, ?)
                """,
                (source, import_path, datetime.now(timezone.utc).isoformat(), "running"),
            )
            return int(cursor.lastrowid)

    def finish_import(
        self,
        import_id: int,
        status: str,
        items_found: int,
        items_imported: int,
        error: str = "",
    ) -> None:
        with self.connection() as conn:
            conn.execute(
                """
                UPDATE imports
                SET finished_at = ?, status = ?, items_found = ?, items_imported = ?, error = ?
                WHERE id = ?
                """,
                (
                    datetime.now(timezone.utc).isoformat(),
                    status,
                    items_found,
                    items_imported,
                    error,
                    import_id,
                ),
            )

    def list_activities(self, limit: int = 100) -> list[Activity]:
        with self.connection() as conn:
            rows = conn.execute(
                """
                SELECT id, source, activity_type, title, body, url, created_at,
                       updated_at, actor, target, metadata
                FROM activities
                ORDER BY created_at DESC, id ASC
                LIMIT ?
                """,
                (limit,),
            ).fetchall()
        return [Activity.from_db_row(dict(row)) for row in rows]

    def get_all_activities(self) -> list[Activity]:
        with self.connection() as conn:
            rows = conn.execute(
                """
                SELECT id, source, activity_type, title, body, url, created_at,
                       updated_at, actor, target, metadata
                FROM activities
                ORDER BY created_at DESC, id ASC
                """
            ).fetchall()
        return [Activity.from_db_row(dict(row)) for row in rows]

    def get_activity_counts(self) -> dict[str, int]:
        with self.connection() as conn:
            rows = conn.execute(
                """
                SELECT activity_type, COUNT(*) AS count
                FROM activities
                GROUP BY activity_type
                ORDER BY count DESC, activity_type ASC
                """
            ).fetchall()
        return {row["activity_type"]: row["count"] for row in rows}

    def get_raw_item_count(self) -> int:
        with self.connection() as conn:
            row = conn.execute("SELECT COUNT(*) AS count FROM raw_items").fetchone()
        return int(row["count"])

    def _ensure_raw_hash(self, conn: sqlite3.Connection) -> None:
        columns = {row["name"] for row in conn.execute("PRAGMA table_info(raw_items)").fetchall()}
        if "raw_hash" not in columns:
            conn.execute("ALTER TABLE raw_items ADD COLUMN raw_hash TEXT")
            rows = conn.execute("SELECT id, source, source_file, raw_json FROM raw_items").fetchall()
            for row in rows:
                conn.execute(
                    "UPDATE raw_items SET raw_hash = ? WHERE id = ?",
                    (build_raw_item_hash(row["source"], row["source_file"], row["raw_json"]), row["id"]),
                )

        conn.execute(
            """
            CREATE UNIQUE INDEX IF NOT EXISTS idx_raw_items_identity
            ON raw_items(source, source_file, raw_hash)
            """
        )


def build_raw_item_hash(source: str, source_file: str, raw_json: str) -> str:
    identity = "|".join([source, source_file, raw_json])
    return sha256(identity.encode("utf-8")).hexdigest()
