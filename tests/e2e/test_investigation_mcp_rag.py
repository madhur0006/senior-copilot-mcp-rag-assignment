"""E2E investigation: MCP tools + RAG in one workflow."""
from __future__ import annotations

import os
from unittest.mock import patch

import httpx
import pytest
from langchain_core.messages import AIMessage, HumanMessage, ToolMessage

from apps.backend.service import run_investigation
from rag.ingestion.config import RagConfig

LIVE_BASE = os.getenv("ALARM_API_BASE_URL", "http://localhost:8000")


def _simulator_up() -> bool:
    try:
        response = httpx.get(f"{LIVE_BASE.rstrip('/')}/health", timeout=2.0)
        return response.status_code == 200
    except Exception:
        return False


def _index_ready(config: RagConfig) -> bool:
    return config.index_dir.exists() and any(config.index_dir.iterdir())


def _openai_configured(config: RagConfig) -> bool:
    return bool(config.openai_key and not config.openai_key.startswith("sk-replace"))


class _FakeAgent:
    def invoke(self, state, config=None):
        query = ""
        messages = state.get("messages") or []
        if messages:
            query = getattr(messages[0], "content", "") or ""
        return {
            "messages": [
                HumanMessage(content=query),
                AIMessage(
                    content="",
                    tool_calls=[
                        {
                            "id": "c1",
                            "name": "search_assets",
                            "args": {"query": "Boiler Feed Pump 101"},
                        },
                        {
                            "id": "c2",
                            "name": "get_recent_critical_alarms",
                            "args": {"asset_id": "AST00001", "days": 90},
                        },
                        {
                            "id": "c3",
                            "name": "search_procedures",
                            "args": {
                                "query": "high discharge pressure response",
                                "doc_id": "OP-BFP-001",
                            },
                        },
                    ],
                ),
                ToolMessage(
                    content='{"total_results":1,"results":[{"asset_id":"AST00001","name":"Boiler Feed Pump 101"}]}',
                    tool_call_id="c1",
                    name="search_assets",
                ),
                ToolMessage(
                    content=(
                        '{"alarms":[{"alarm_id":"ALM0035590","severity":"high",'
                        '"alarm_name":"Pump Discharge Pressure High","asset_id":"AST00001"}]}'
                    ),
                    tool_call_id="c2",
                    name="get_recent_critical_alarms",
                ),
                ToolMessage(
                    content=(
                        '{"confidence":"high","citations":[{"doc_id":"OP-BFP-001",'
                        '"section":"8.1 High or critical discharge pressure",'
                        '"source_path":"operating-procedures/OP-BFP-001-boiler-feed-pump-operation.pdf",'
                        '"excerpt":"Acknowledge the alarm and check a second reading."}],'
                        '"excerpts":[{"doc_id":"OP-BFP-001","section":"8.1","text":"Open recirculation if confirmed high."}]}'
                    ),
                    tool_call_id="c3",
                    name="search_procedures",
                ),
                AIMessage(
                    content=(
                        "BFP-101 shows recurring high discharge pressure (ALM0035590). "
                        "Follow OP-BFP-001 section 8.1: confirm reading, then open recirculation."
                    )
                ),
            ]
        }


def test_e2e_investigation_combines_mcp_and_rag_mocked():
    with patch("apps.backend.service.build_agent", return_value=_FakeAgent()):
        with patch("apps.backend.service.list_mcp_tools", return_value=[]):
            result = run_investigation(
                "Investigate recurring high-severity alarms for Boiler Feed Pump 101 "
                "over the last 90 days.",
                discover_tools=False,
            )

    tool_names = [t.tool for t in result.tool_trace]
    assert "search_assets" in tool_names
    assert "get_recent_critical_alarms" in tool_names
    assert "search_procedures" in tool_names
    assert result.citations
    assert result.citations[0]["doc_id"] == "OP-BFP-001"
    assert result.alarms
    assert result.alarms[0]["alarm_id"] == "ALM0035590"
    assert "OP-BFP-001" in result.answer
    assert "8.1" in result.answer


@pytest.mark.skipif(not _simulator_up(), reason="Alarm API simulator not running")
def test_e2e_live_bfp_investigation_mcp_and_rag():
    config = RagConfig()
    if not _index_ready(config):
        pytest.skip("RAG index missing")
    if not _openai_configured(config):
        pytest.skip("OPENAI_API_KEY not configured")

    result = run_investigation(
        "Investigate recurring high-severity alarms for Boiler Feed Pump 101 "
        "over the last 90 days. Summarize top alarms and cite OP-BFP-001 or SI-BFP-031.",
        config=config,
        discover_tools=False,
    )

    tool_names = {t.tool for t in result.tool_trace}
    assert tool_names & {
        "search_assets",
        "get_alarms",
        "get_recent_critical_alarms",
        "get_asset_metadata",
    }, f"expected MCP alarm tools, got {tool_names}"
    assert "search_procedures" in tool_names or result.citations, (
        "expected RAG tool or citations"
    )
    assert result.answer and len(result.answer) > 40
    assert any(t.ok for t in result.tool_trace)
