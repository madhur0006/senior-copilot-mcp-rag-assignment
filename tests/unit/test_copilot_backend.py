"""Unit tests for Step 6 MCP client helpers (mocked)."""
from unittest.mock import patch

from apps.backend.mcp_client import call_mcp_tool, call_mcp_tool_json
from apps.backend.models import InvestigationResult, ToolTraceItem
from apps.backend.service import _extract_trace, _final_answer
from langchain_core.messages import AIMessage, HumanMessage, ToolMessage


def test_call_mcp_tool_returns_error_dict_on_failure():
    with patch(
        "apps.backend.mcp_client._call_tool_async",
        side_effect=RuntimeError("boom"),
    ):
        result = call_mcp_tool("search_assets", {"query": "x"})
    assert result["error"] is True
    assert result["tool"] == "search_assets"


def test_call_mcp_tool_json_serializes():
    with patch(
        "apps.backend.mcp_client.call_mcp_tool",
        return_value={"items": [{"id": "AST1"}]},
    ):
        text = call_mcp_tool_json("search_assets", {"query": "bfp"})
    assert "AST1" in text


def test_extract_trace_and_citations():
    messages = [
        HumanMessage(content="q"),
        AIMessage(
            content="",
            tool_calls=[
                {
                    "id": "1",
                    "name": "search_procedures",
                    "args": {"query": "bfp"},
                }
            ],
        ),
        ToolMessage(
            content='{"citations":[{"doc_id":"OP-BFP-001","section":"8.1"}],"confidence":"high"}',
            tool_call_id="1",
            name="search_procedures",
        ),
        AIMessage(content="Final answer citing OP-BFP-001."),
    ]
    trace, citations = _extract_trace(messages)
    assert trace[0].tool == "search_procedures"
    assert citations[0]["doc_id"] == "OP-BFP-001"
    assert _final_answer(messages).startswith("Final answer")


def test_investigation_result_to_dict():
    result = InvestigationResult(
        query="q",
        answer="a",
        tool_trace=[ToolTraceItem(tool="search_assets", arguments={"query": "x"})],
        citations=[{"doc_id": "OP-BFP-001"}],
        mcp_tools_discovered=["search_assets"],
    )
    data = result.to_dict()
    assert data["answer"] == "a"
    assert data["tool_trace"][0]["tool"] == "search_assets"
