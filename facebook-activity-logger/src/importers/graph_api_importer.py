from __future__ import annotations

from datetime import datetime

import requests

from src.database import Database
from src.models import Activity, normalize_activity_type


class GraphAPIImporter:
    GRAPH_API_BASE = "https://graph.facebook.com/v22.0"

    def __init__(self, database: Database, access_token: str) -> None:
        self.database = database
        self.access_token = access_token.strip()

    def import_since(self, since_date: str) -> dict:
        if not self.access_token:
            raise ValueError("FACEBOOK_ACCESS_TOKEN is required for Graph API import.")

        datetime.strptime(since_date, "%Y-%m-%d")

        import_id = self.database.start_import(source="graph_api", import_path=f"graph_api?since={since_date}")
        items_found = 0
        items_imported = 0

        try:
            url = f"{self.GRAPH_API_BASE}/me/posts"
            params = {
                "access_token": self.access_token,
                "since": since_date,
                "fields": "id,message,created_time,permalink_url",
                "limit": 100,
            }

            while url:
                response = requests.get(url, params=params, timeout=20)
                response.raise_for_status()
                payload = response.json()

                for post in payload.get("data", []):
                    items_found += 1
                    created_at = post.get("created_time", "")
                    body = post.get("message", "")
                    post_id = post.get("id", "")
                    activity = Activity(
                        id=post_id
                        or Activity.build_id(
                            "graph_api",
                            "posts",
                            created_at,
                            body[:100],
                            body,
                            "graph_api:/me/posts",
                        ),
                        source="graph_api",
                        activity_type=normalize_activity_type("posts"),
                        title=(body[:100] if body else "Graph API Post"),
                        body=body,
                        url=post.get("permalink_url", ""),
                        created_at=created_at,
                        updated_at=created_at,
                        actor="self",
                        target="",
                        metadata={"graph_object": "post"},
                    )

                    inserted = self.database.insert_activity(activity)
                    if inserted:
                        items_imported += 1

                    self.database.insert_raw_item(
                        source="graph_api",
                        source_file="graph_api:/me/posts",
                        activity_id=activity.id,
                        raw_item=post,
                    )

                url = payload.get("paging", {}).get("next", "")
                params = {}

            self.database.finish_import(
                import_id=import_id,
                status="completed",
                items_found=items_found,
                items_imported=items_imported,
            )

            return {
                "import_id": import_id,
                "source": "graph_api",
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
