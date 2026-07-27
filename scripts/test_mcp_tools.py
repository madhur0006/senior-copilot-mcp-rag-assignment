"""Smoke test MCP tools against the live Alarm API simulator.

  PYTHONPATH=. python3 scripts/test_mcp_tools.py
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

SERVER_DIR = ROOT / "mcp-servers" / "alarm-management"
if str(SERVER_DIR) not in sys.path:
    sys.path.insert(0, str(SERVER_DIR))

from server import (  # noqa: E402
    calculate_alarm_priority,
    correlate_alarms,
    get_alarms,
    get_asset_metadata,
    get_operator_recommendations,
    get_recent_critical_alarms,
    search_assets,
)


def main():
    print("MCP tool smoke test")

    result = search_assets("Boiler Feed Pump 101", limit=3)
    print(f"search_assets: {result.get('total_results')} results")
    if not result.get("results"):
        print("No assets found; is the simulator running?")
        return

    asset_id = result["results"][0]["asset_id"]
    print(f"asset_id: {asset_id}")

    meta = get_asset_metadata(asset_id)
    print(f"related_assets: {len(meta.get('related_assets', []))}")

    alarms = get_recent_critical_alarms(asset_id, days=90)
    alarm_rows = alarms.get("data") or []
    print(f"recent critical alarms: {len(alarm_rows)}")

    if alarm_rows:
        alarm_id = alarm_rows[0]["alarm_id"]
        priority = calculate_alarm_priority(alarm_id)
        print(f"priority_score: {priority.get('priority_score')}")
        recs = get_operator_recommendations(alarm_id)
        print(f"recommendations: {len(recs.get('recommended_actions', []))}")

    corr = correlate_alarms([asset_id], days=90)
    print(f"correlation_groups: {len(corr.get('correlation_groups', []))}")

    filtered = get_alarms(asset_id=asset_id, severity="high", page_size=5)
    print(f"filtered alarms: {len(filtered.get('data', []))}")
    print("done")


if __name__ == "__main__":
    main()
