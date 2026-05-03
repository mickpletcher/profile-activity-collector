from __future__ import annotations

import logging
from pathlib import Path

from src.config import redact_sensitive_fields
from src.database import Database
from src.parsers.json_parser import parse_archive_file

logger = logging.getLogger(__name__)


class XArchiveImporter:
    def __init__(self, database: Database) -> None:
        self.database = database

    def import_from_path(self, import_path: Path) -> dict:
        import_path = import_path.resolve()
        import_id = self.database.start_import(source="x_archive", import_path=import_path.as_posix())

        items_found = 0
        items_imported = 0

        try:
            archive_files = sorted(import_path.rglob("*.json")) + sorted(import_path.rglob("*.js"))
            for archive_file in archive_files:
                parsed_activities = parse_archive_file(archive_file, source="x_archive")
                items_found += len(parsed_activities)

                for parsed in parsed_activities:
                    inserted = self.database.insert_activity(parsed.activity)
                    if inserted:
                        items_imported += 1

                    self.database.insert_raw_item(
                        source="x_archive",
                        source_file=parsed.source_file,
                        activity_id=parsed.activity.id,
                        raw_item=parsed.raw_item,
                    )

                logger.info(
                    "Processed X archive file",
                    extra={
                        "details": redact_sensitive_fields(
                            {
                                "file": archive_file.as_posix(),
                                "parsed_activities": len(parsed_activities),
                            }
                        )
                    },
                )

            self.database.finish_import(
                import_id=import_id,
                status="completed",
                items_found=items_found,
                items_imported=items_imported,
            )

            return {
                "import_id": import_id,
                "source": "x_archive",
                "items_found": items_found,
                "items_imported": items_imported,
            }
        except Exception as exc:
            self.database.finish_import(
                import_id=import_id,
                status="failed",
                items_found=items_found,
                items_imported=items_imported,
                error=str(exc),
            )
            raise
