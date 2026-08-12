"""MCP client and agent unit tests."""
from __future__ import annotations

from types import SimpleNamespace
from unittest.mock import MagicMock, patch

from apps.backend.agent import SYSTEM_PROMPT, build_agent
from apps.backend.mcp_client import _extract_tool_payload, list_mcp_tools
from apps.backend.tools import COPILOT_TOOLS
from rag.ingestion.config import RagConfig


def test_extract_tool_payload_from_data_attr():
    result = SimpleNamespace(data={"asset_id": "AST1"}, content=None)
    assert _extract_tool_payload(result) == {"asset_id": "AST1"}


def test_extract_tool_payload_from_json_text_block():
    block = SimpleNamespace(text='{"ok": true}')
    result = SimpleNamespace(data=None, structured_content=None, content=[block])
    assert _extract_tool_payload(result) == {"ok": True}


def test_extract_tool_payload_plain_dict():
    assert _extract_tool_payload({"a": 1}) == {"a": 1}
    assert _extract_tool_payload(None) is None


@patch("apps.backend.mcp_client._list_tools_async")
@patch("apps.backend.mcp_client.asyncio.run")
def test_list_mcp_tools_sync_wrapper(mock_run, mock_async_fn):
    mock_async_fn.return_value = None
    mock_run.return_value = [
        {"name": "search_assets", "description": "find assets"}
    ]
    tools = list_mcp_tools()
    assert tools[0]["name"] == "search_assets"
    mock_run.assert_called_once()


@patch("apps.backend.agent.ChatOpenAI")
def test_build_agent_registers_tools(mock_chat):
    llm = MagicMock()
    llm.bind_tools.return_value = llm
    mock_chat.return_value = llm
    config = RagConfig(OPENAI_API_KEY="sk-test")
    agent = build_agent(config)
    assert agent is not None
    llm.bind_tools.assert_called_once()
    bound = llm.bind_tools.call_args[0][0]
    assert len(bound) == len(COPILOT_TOOLS)
    assert "search_assets" in SYSTEM_PROMPT
    assert "search_procedures" in SYSTEM_PROMPT
