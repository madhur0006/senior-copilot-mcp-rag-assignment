"""
Unit tests for MCP server tools.
Mocks the AlarmApiClient to test tool logic.
"""
import sys
from pathlib import Path
from unittest.mock import Mock, patch

import pytest

# Add project root to path
ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


def test_mcp_server_tools_exist():
    """Test that MCP server tools can be imported."""
    # Import the server module directly
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "server",
        ROOT / "mcp-servers" / "alarm-management" / "server.py"
    )
    server_module = importlib.util.module_from_spec(spec)
    
    # Check that tools exist
    assert hasattr(server_module, 'search_assets')
    assert hasattr(server_module, 'get_asset_metadata')
    assert hasattr(server_module, 'get_alarms')
    assert hasattr(server_module, 'correlate_alarms')
    assert hasattr(server_module, 'calculate_alarm_priority')
    assert hasattr(server_module, 'get_operator_recommendations')
