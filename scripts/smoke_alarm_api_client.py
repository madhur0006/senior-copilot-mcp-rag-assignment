"""Smoke script for Step 3 — Alarm API connector against local simulator.

Usage:
  PYTHONPATH=. python scripts/smoke_alarm_api_client.py
  # or: make smoke-alarm-api
"""

from __future__ import annotations

import json
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from connectors.alarm_api import AlarmApiClient, AlarmApiConfig


def main() -> None:
    config = AlarmApiConfig()
    with AlarmApiClient(config) as client:
        print("health:", json.dumps(client.health(), indent=2))

        search = client.search_assets("Boiler Feed Pump 101", limit=3, trace_id="step3-smoke")
        print("search total:", search.get("total_results"))
        asset = search["results"][0]
        asset_id = asset["asset_id"]
        print("asset:", asset_id, asset.get("asset_name"))

        meta = client.get_asset_metadata(asset_id, trace_id="step3-smoke")
        print("related_assets:", meta.get("related_assets"))

        end = datetime.now(timezone.utc)
        start = end - timedelta(days=90)
        alarms = client.get_alarms(
            asset_id=asset_id,
            severity=["high", "critical"],
            start_time=start.isoformat().replace("+00:00", "Z"),
            end_time=end.isoformat().replace("+00:00", "Z"),
            page_size=5,
            trace_id="step3-smoke",
        )
        print("alarms returned:", len(alarms.get("data", [])))
        if alarms.get("data"):
            alarm_id = alarms["data"][0]["alarm_id"]
            print("first alarm:", alarm_id, alarms["data"][0].get("alarm_name"))
            priority = client.get_priority_score(alarm_id, trace_id="step3-smoke")
            print("priority keys:", sorted(priority.keys()))
            recs = client.get_operator_recommendations(alarm_id, trace_id="step3-smoke")
            print("recommendation keys:", sorted(recs.keys()))

        correlation = client.correlate_alarms(
            {
                "asset_ids": [asset_id],
                "time_range": {
                    "start_time": start.isoformat().replace("+00:00", "Z"),
                    "end_time": end.isoformat().replace("+00:00", "Z"),
                },
                "correlation_method": "cooccurrence",
                "lag_window_minutes": 15,
                "severity_threshold": "medium",
                "min_support": 1,
            },
            trace_id="step3-smoke",
        )
        print("correlation keys:", sorted(correlation.keys()))
        print("SMOKE OK")


if __name__ == "__main__":
    main()
