"""MCP server for the Alarm Management API."""
import sys
from pathlib import Path
from datetime import datetime, timedelta, timezone

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from fastmcp import FastMCP
from connectors.alarm_api import AlarmApiClient, AlarmApiConfig

mcp = FastMCP("alarm-management")
alarm_client = None


def get_client():
    global alarm_client
    if alarm_client is None:
        config = AlarmApiConfig()
        alarm_client = AlarmApiClient(config)
    return alarm_client


@mcp.tool()
def search_assets(query: str, site: str = None, unit: str = None, limit: int = 25) -> dict:
    """Search for assets by name or ID."""
    client = get_client()
    return client.search_assets(query, site=site, unit=unit, limit=limit)


@mcp.tool()
def get_asset_metadata(asset_id: str) -> dict:
    """Get detailed metadata for an asset (e.g. AST00001)."""
    client = get_client()
    return client.get_asset_metadata(asset_id)


@mcp.tool()
def get_alarms(
    asset_id: str = None,
    severity: str = None,
    status: str = None,
    page: int = 1,
    page_size: int = 50,
) -> dict:
    """List alarms with optional asset, severity, and status filters."""
    client = get_client()
    # API expects severity as a list
    severity_list = [severity] if severity else None
    return client.get_alarms(
        asset_id=asset_id,
        severity=severity_list,
        status=status,
        page=page,
        page_size=page_size,
    )


@mcp.tool()
def get_recent_critical_alarms(asset_id: str, days: int = 7) -> dict:
    """Get high/critical alarms for an asset over the last N days."""
    client = get_client()
    end = datetime.now(timezone.utc)
    start = end - timedelta(days=days)
    return client.get_alarms(
        asset_id=asset_id,
        severity=["high", "critical"],
        start_time=start.isoformat().replace("+00:00", "Z"),
        end_time=end.isoformat().replace("+00:00", "Z"),
        page_size=50,
    )


@mcp.tool()
def correlate_alarms(asset_ids: list, days: int = 7) -> dict:
    """Correlate alarms across assets over the last N days."""
    client = get_client()
    end = datetime.now(timezone.utc)
    start = end - timedelta(days=days)
    payload = {
        "asset_ids": asset_ids,
        "time_range": {
            "start_time": start.isoformat().replace("+00:00", "Z"),
            "end_time": end.isoformat().replace("+00:00", "Z"),
        },
        "correlation_method": "cooccurrence",
        "lag_window_minutes": 15,
        "severity_threshold": "medium",
        "min_support": 1,
    }
    return client.correlate_alarms(payload)


@mcp.tool()
def calculate_alarm_priority(alarm_id: str) -> dict:
    """Calculate priority score for an alarm."""
    client = get_client()
    return client.get_priority_score(alarm_id)


@mcp.tool()
def get_operator_recommendations(alarm_id: str) -> dict:
    """Get recommended operator actions for an alarm."""
    client = get_client()
    return client.get_operator_recommendations(alarm_id)


if __name__ == "__main__":
    mcp.run()
