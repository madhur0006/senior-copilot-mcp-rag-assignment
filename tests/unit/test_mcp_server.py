"""MCP server tool registration tests."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


def test_mcp_server_tools_exist():
    import importlib.util

    spec = importlib.util.spec_from_file_location(
        "server",
        ROOT / "mcp-servers" / "alarm-management" / "server.py",
    )
    server_module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(server_module)
    assert hasattr(server_module, "search_assets")
    assert hasattr(server_module, "get_asset_metadata")
    assert hasattr(server_module, "get_alarms")
    assert hasattr(server_module, "correlate_alarms")
    assert hasattr(server_module, "calculate_alarm_priority")
    assert hasattr(server_module, "get_operator_recommendations")
