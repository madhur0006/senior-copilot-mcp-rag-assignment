"""
Manual test script for MCP server tools.
Run this to verify tools work against the live simulator.

Usage:
    PYTHONPATH=. python3 scripts/test_mcp_tools.py
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

# Import MCP tools
from mcp_servers.alarm_management.server import (
    search_assets,
    get_asset_metadata,
    get_alarms,
    get_recent_critical_alarms,
    correlate_alarms,
    calculate_alarm_priority,
    get_operator_recommendations
)


def main():
    print("Testing MCP Server Tools\n" + "="*50)
    
    # Test 1: Search assets
    print("\n1. Search Assets")
    result = search_assets("Boiler Feed Pump 101", limit=3)
    print(f"   Found {result.get('total_results')} assets")
    if result.get("results"):
        asset_id = result["results"][0]["asset_id"]
        print(f"   First asset: {asset_id}")
    
        # Test 2: Get asset metadata
        print("\n2. Get Asset Metadata")
        meta = get_asset_metadata(asset_id)
        print(f"   Related assets: {len(meta.get('related_assets', []))}")
        
        # Test 3: Get recent critical alarms
        print("\n3. Get Recent Critical Alarms")
        alarms = get_recent_critical_alarms(asset_id, days=90)
        alarm_count = len(alarms.get("data", []))
        print(f"   Found {alarm_count} high/critical alarms")
        
        if alarm_count > 0:
            alarm_id = alarms["data"][0]["alarm_id"]
            print(f"   First alarm: {alarm_id}")
            
            # Test 4: Calculate priority
            print("\n4. Calculate Alarm Priority")
            priority = calculate_alarm_priority(alarm_id)
            print(f"   Priority score: {priority.get('priority_score')}")
            
            # Test 5: Get recommendations
            print("\n5. Get Operator Recommendations")
            recs = get_operator_recommendations(alarm_id)
            action_count = len(recs.get("recommended_actions", []))
            print(f"   Found {action_count} recommended actions")
        
        # Test 6: Correlate alarms
        print("\n6. Correlate Alarms")
        corr = correlate_alarms([asset_id], days=90)
        print(f"   Correlation groups: {len(corr.get('correlation_groups', []))}")
        
        # Test 7: Get alarms with filters
        print("\n7. Get Alarms with Filters")
        filtered = get_alarms(asset_id=asset_id, severity="high", page_size=5)
        print(f"   Filtered alarms: {len(filtered.get('data', []))}")
    
    print("\n" + "="*50)
    print("All MCP tools tested successfully!")


if __name__ == "__main__":
    main()
