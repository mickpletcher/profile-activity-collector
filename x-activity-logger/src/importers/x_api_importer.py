from __future__ import annotations

from datetime import datetime

import requests

from src.database import Database
from src.models import Activity, normalize_activity_type


class XAPIImporter:
    API_BASE = "https://api.x.com/2"

    def __init__(self, database: Database, bearer_token: str, user_id: str) -> None:
        self.database = database
        self.bearer_token = bearer_token.strip()
        self.user_id = user_id.strip()

    def import_since(self, since_date: str) -> dict:
        if not self.bearer_token:
            raise ValueError("X_API_BEARER_TOKEN is required for API import.")
        if not self.user_id:
            raise ValueError("X_USER_ID is required for API import.")

        datetime.strptime(since_date, "%Y-%m-%d")

        import_id = self.database.start_import(source="x_api", import_path=f"x_api?since={since_date}")
        items_found = 0
        items_imported = 0

        try:
            url = f"{self.API_BASE}/users/{self.user_id}/tweets"
            headers = {"Authorization": f"Bearer {self.bearer_token}"}
            params = {
                "max_results": 100,
                "start_time": f"{since_date}T00:00:00Z",
                "tweet.fields": "created_at,public_metrics,conversation_id",
            }

            while True:
                response = requests.get(url, headers=headers, params=params, timeout=20)
                response.raise_for_status()
                payload = response.json()

                for tweet in payload.get("data", []):
                    items_found += 1
                    body = tweet.get("text", "")
                    created_at = tweet.get("created_at", "")
                    tweet_id = tweet.get("id", "")
                    activity = Activity(
                        id=tweet_id
                        or Activity.build_id(
                            "x_api",
                            "tweets",
                            created_at,
                            body[:60],
                            body,
                            "x_api:/tweets",
                        ),
                        source="x_api",
                        activity_type=normalize_activity_type("tweets"),
                        title=(body[:100] if body else "API Tweet"),
                        body=body,
                        url=(f"https://x.com/i/web/status/{tweet_id}" if tweet_id else ""),
                        created_at=created_at,
                        updated_at=created_at,
                        actor=self.user_id,
                        target=tweet.get("conversation_id", ""),
                        metadata={"public_metrics": tweet.get("public_metrics", {})},
                    )

                    inserted = self.database.insert_activity(activity)
                    if inserted:
                        items_imported += 1

                    self.database.insert_raw_item(
                        source="x_api",
                        source_file=f"x_api:/users/{self.user_id}/tweets",
                        activity_id=activity.id,
                        raw_item=tweet,
                    )

                next_token = payload.get("meta", {}).get("next_token")
                if not next_token:
                    break
                params["pagination_token"] = next_token

            self.database.finish_import(
                import_id=import_id,
                status="completed",
                items_found=items_found,
                items_imported=items_imported,
            )

            return {
                "import_id": import_id,
                "source": "x_api",
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
