from __future__ import annotations

from datetime import datetime

import requests

from src.database import Database
from src.models import Activity, normalize_activity_type


class LinkedInAPIImporter:
    API_BASE = "https://api.linkedin.com/v2"

    def __init__(self, database: Database, access_token: str, person_urn: str) -> None:
        self.database = database
        self.access_token = access_token.strip()
        self.person_urn = person_urn.strip()

    def import_since(self, since_date: str) -> dict:
        if not self.access_token:
            raise ValueError("LINKEDIN_ACCESS_TOKEN is required for API import.")
        if not self.person_urn:
            raise ValueError("LINKEDIN_PERSON_URN is required for API import.")

        datetime.strptime(since_date, "%Y-%m-%d")

        import_id = self.database.start_import(source="linkedin_api", import_path=f"linkedin_api?since={since_date}")
        items_found = 0
        items_imported = 0

        try:
            url = f"{self.API_BASE}/ugcPosts"
            headers = {
                "Authorization": f"Bearer {self.access_token}",
                "X-Restli-Protocol-Version": "2.0.0",
            }
            params = {
                "q": "authors",
                "authors": f"List({self.person_urn})",
                "count": 100,
            }

            response = requests.get(url, headers=headers, params=params, timeout=20)
            response.raise_for_status()
            payload = response.json()

            for item in payload.get("elements", []):
                items_found += 1
                created_at_ms = item.get("created", {}).get("time")
                created_at = str(created_at_ms) if created_at_ms else ""
                activity = Activity(
                    id=item.get("id", "") or Activity.build_id("linkedin_api", "posts", created_at, "ugc post", "", "api"),
                    source="linkedin_api",
                    activity_type=normalize_activity_type("posts"),
                    title="LinkedIn UGC Post",
                    body="",
                    url="",
                    created_at=created_at,
                    updated_at=created_at,
                    actor=self.person_urn,
                    target="",
                    metadata={"lifecycleState": item.get("lifecycleState", "")},
                )

                inserted = self.database.insert_activity(activity)
                if inserted:
                    items_imported += 1

                self.database.insert_raw_item(
                    source="linkedin_api",
                    source_file="linkedin_api:/ugcPosts",
                    activity_id=activity.id,
                    raw_item=item,
                )

            self.database.finish_import(
                import_id=import_id,
                status="completed",
                items_found=items_found,
                items_imported=items_imported,
            )

            return {
                "import_id": import_id,
                "source": "linkedin_api",
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
