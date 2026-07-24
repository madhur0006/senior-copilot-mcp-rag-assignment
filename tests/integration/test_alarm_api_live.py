from __future__ import annotations

import os
from datetime import datetime, timedelta, timezone

import httpx
import pytest

from connectors.alarm_api import AlarmApiAuthError, AlarmApiClient, AlarmApiConfig

LIVE_BASE = os.getenv("ALARM_API_BASE_URL", "http://localhost:8000")


def _simulator_up() -> bool:
    try:
        response = httpx.get(f"{LIVE_BASE.rstrip('/')}/health", timeout=2.0)
        return response.status_code == 200
    except Exception:
        return False


pytestmark = pytest.mark.skipif(
    not _simulator_up(),
    reason="Alarm API simulator is not running on ALARM_API_BASE_URL",
)


@pytest.fixture
def client() -> AlarmApiClient:
    config = AlarmApiConfig(
        ALARM_API_BASE_URL=LIVE_BASE,
        ALARM_API_TOKEN=os.getenv("ALARM_API_TOKEN", "demo-token"),
    )
    with AlarmApiClient(config) as c:
        yield c


def test_live_health(client: AlarmApiClient) -> None:
    data = client.health()
    assert data.get("status") == "ok"


def test_live_auth_required_for_alarms() -> None:
    bad = AlarmApiConfig(ALARM_API_BASE_URL=LIVE_BASE, ALARM_API_TOKEN="")
    # Empty bearer still sends header; simulator checks non-empty. Use no-auth request path.
    with AlarmApiClient(bad) as client:
        with pytest.raises(AlarmApiAuthError):
            # force unauthenticated call
            client.request("GET", "/alarms", auth=False)


def test_live_search_metadata_alarms_chain(client: AlarmApiClient) -> None:
    search = client.search_assets("Boiler Feed Pump 101", limit=5, trace_id="step3-live")
    assert search["total_results"] >= 1
    asset_id = search["results"][0]["asset_id"]

    meta = client.get_asset_metadata(asset_id, trace_id="step3-live")
    assert meta["asset_id"] == asset_id
    assert "related_assets" in meta

    end = datetime.now(timezone.utc)
    start = end - timedelta(days=90)
    alarms = client.get_alarms(
        asset_id=asset_id,
        page_size=5,
        start_time=start.isoformat().replace("+00:00", "Z"),
        end_time=end.isoformat().replace("+00:00", "Z"),
        trace_id="step3-live",
    )
    assert "data" in alarms

    if alarms["data"]:
        alarm_id = alarms["data"][0]["alarm_id"]
        priority = client.get_priority_score(alarm_id, trace_id="step3-live")
        assert isinstance(priority, dict)
        recs = client.get_operator_recommendations(alarm_id, trace_id="step3-live")
        assert isinstance(recs, dict)

    correlation = client.correlate_alarms(
        {
            "asset_ids": [asset_id],
            "time_range": {
                "start_time": start.isoformat().replace("+00:00", "Z"),
                "end_time": end.isoformat().replace("+00:00", "Z"),
            },
            "min_support": 1,
        },
        trace_id="step3-live",
    )
    assert isinstance(correlation, dict)
