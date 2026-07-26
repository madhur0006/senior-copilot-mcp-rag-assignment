"""
MCP Server for Alarm Management API.
Exposes alarm investigation tools via Model Context Protocol.
"""
import sys
from pathlib import Path
from datetime import datetime, timedelta, timezone

# Add project root to path
ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from fastmcp import FastMCP
from connectors.alarm_api import AlarmApiClient, AlarmApiConfig

# Initialize MCP server
mcp = FastMCP("alarm-management")

# Create shared alarm API client
alarm_client = None


def get_client():
    """Get or create the alarm API client."""
    global alarm_client
    if alarm_client is None:
        config = AlarmApiConfig()
        alarm_client = AlarmApiClient(config)
    return alarm_client


@mcp.tool()
def search_assets(query: str, site: str = None, unit: str = None, limit: int = 25) -> dict:
    """
    Search for assets by name or ID.
    
    Args:
        query: Search text (asset name or ID)
        site: Optional site filter
        unit: Optional unit filter
        limit: Maximum results to return
    
    Returns:
        Dictionary with search results and total count
    """
    client = get_client()
    return client.search_assets(query, site=site, unit=unit, limit=limit)


@mcp.tool()
def get_asset_metadata(asset_id: str) -> dict:
    """
    Get detailed metadata for a specific asset.
    
    Args:
        asset_id: The asset ID (e.g., AST00001)
    
    Returns:
        Dictionary with asset details, tags, and related assets
    """
    client = get_client()
    return client.get_asset_metadata(asset_id)


@mcp.tool()
def get_alarms(
    asset_id: str = None,
    severity: str = None,
    status: str = None,
    page: int = 1,
    page_size: int = 50
) -> dict:
    """
    Get list of alarms with optional filters.
    
    Args:
        asset_id: Filter by asset ID
        severity: Filter by severity (low, medium, high, critical)
        status: Filter by status (active, acknowledged, resolved)
        page: Page number for pagination
        page_size: Number of results per page
    
    Returns:
        Dictionary with alarm list and pagination info
    """
    client = get_client()
    
    # Convert single severity to list if provided
    severity_list = [severity] if severity else None
    
    return client.get_alarms(
        asset_id=asset_id,
        severity=severity_list,
        status=status,
        page=page,
        page_size=page_size
    )


@mcp.tool()
def get_recent_critical_alarms(asset_id: str, days: int = 7) -> dict:
    """
    Get recent high/critical alarms for an asset.
    Convenience tool that filters by severity and time range.
    
    Args:
        asset_id: The asset ID
        days: Number of days to look back (default 7)
    
    Returns:
        Dictionary with filtered alarm list
    """
    client = get_client()
    
    end = datetime.now(timezone.utc)
    start = end - timedelta(days=days)
    
    return client.get_alarms(
        asset_id=asset_id,
        severity=["high", "critical"],
        start_time=start.isoformat().replace("+00:00", "Z"),
        end_time=end.isoformat().replace("+00:00", "Z"),
        page_size=50
    )


@mcp.tool()
def correlate_alarms(asset_ids: list, days: int = 7) -> dict:
    """
    Find correlations between alarms across multiple assets.
    
    Args:
        asset_ids: List of asset IDs to analyze
        days: Number of days to look back (default 7)
    
    Returns:
        Dictionary with correlation groups and patterns
    """
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
    """
    Calculate priority score for an alarm.
    
    Args:
        alarm_id: The alarm ID
    
    Returns:
        Dictionary with priority score and contributing factors
    """
    client = get_client()
    return client.get_priority_score(alarm_id)


@mcp.tool()
def get_operator_recommendations(alarm_id: str) -> dict:
    """
    Get recommended operator actions for an alarm.
    
    Args:
        alarm_id: The alarm ID
    
    Returns:
        Dictionary with recommended actions and context
    """
    client = get_client()
    return client.get_operator_recommendations(alarm_id)


if __name__ == "__main__":
    # Run with stdio transport (for local use with MCP clients)
    mcp.run()
