"""Copilot tool unit tests (mocked MCP and RAG)."""
from __future__ import annotations

import json
from unittest.mock import patch

from langchain_core.documents import Document

from apps.backend.tools import (
    _compact_alarm_payload,
    _dump,
    calculate_alarm_priority,
    correlate_alarms,
    get_alarms,
    get_asset_metadata,
    get_operator_recommendations,
    get_recent_critical_alarms,
    search_assets,
    search_procedures,
)
from rag.retrieval.retriever import RetrievalResult


def test_dump_truncates_long_payload():
    big = {"x": "a" * 7000}
    text = _dump(big, max_chars=200)
    assert len(text) <= 200
    assert "truncated" in text


def test_compact_alarm_payload_limits_rows():
    payload = {
        "data": [
            {"alarm_id": f"A{i}", "severity": "high", "noise": "drop-me"}
            for i in range(20)
        ]
    }
    out = _compact_alarm_payload(payload, limit=3)
    assert out["count_returned"] == 3
    assert out["count_total_estimate"] == 20
    assert "noise" not in out["alarms"][0]
    assert out["alarms"][0]["alarm_id"] == "A0"


def test_compact_alarm_payload_error_passthrough():
    err = {"error": True, "message": "boom"}
    assert _compact_alarm_payload(err) == err


@patch("apps.backend.tools.call_mcp_tool")
def test_search_assets_passes_filters(mock_call):
    mock_call.return_value = {"total_results": 1, "results": [{"asset_id": "AST1"}]}
    text = search_assets.invoke(
        {"query": "BFP", "site": "EastRefinery", "unit": "Unit 2", "limit": 50}
    )
    args = mock_call.call_args[0][1]
    assert args["query"] == "BFP"
    assert args["site"] == "EastRefinery"
    assert args["limit"] == 10
    assert "AST1" in text


@patch("apps.backend.tools.call_mcp_tool")
def test_get_asset_metadata_and_priority_and_recs(mock_call):
    mock_call.return_value = {"ok": True}
    assert "ok" in get_asset_metadata.invoke({"asset_id": "AST00001"})
    assert "ok" in calculate_alarm_priority.invoke({"alarm_id": "ALM1"})
    assert "ok" in get_operator_recommendations.invoke({"alarm_id": "ALM1"})
    assert mock_call.call_count == 3


@patch("apps.backend.tools.call_mcp_tool")
def test_get_alarms_and_recent_critical_compact(mock_call):
    mock_call.return_value = {
        "data": [
            {"alarm_id": "ALM1", "severity": "high", "extra": 1},
            {"alarm_id": "ALM2", "severity": "critical"},
        ]
    }
    alarms = json.loads(
        get_alarms.invoke({"asset_id": "AST00001", "severity": "high", "page_size": 99})
    )
    assert alarms["count_returned"] == 2
    assert "extra" not in alarms["alarms"][0]

    recent = json.loads(
        get_recent_critical_alarms.invoke({"asset_id": "AST00001", "days": 90})
    )
    assert recent["alarms"][0]["alarm_id"] == "ALM1"


@patch("apps.backend.tools.call_mcp_tool")
def test_correlate_alarms_splits_ids(mock_call):
    mock_call.return_value = {"correlation_groups": []}
    correlate_alarms.invoke({"asset_ids": "AST1, AST2, ,AST3", "days": 30})
    args = mock_call.call_args[0][1]
    assert args["asset_ids"] == ["AST1", "AST2", "AST3"]
    assert args["days"] == 30


@patch("apps.backend.tools.retrieve_detailed")
def test_search_procedures_skips_ast_asset_and_prefers_sections(mock_retrieve):
    intro = Document(
        page_content="intro text",
        metadata={"doc_id": "OP-BFP-001", "section": "Introduction"},
    )
    body = Document(
        page_content="Open recirculation if confirmed high.",
        metadata={
            "doc_id": "OP-BFP-001",
            "section": "8.1 High or critical discharge pressure",
        },
    )
    mock_retrieve.return_value = RetrievalResult(
        query="q",
        documents=[intro, body],
        citations=[],
        scores=[0.2, 0.1],
        confidence="high",
        reason="ok",
    )
    text = search_procedures.invoke(
        {
            "query": "discharge pressure",
            "asset": "AST00001",
            "doc_id": "OP-BFP-001",
            "k": 1,
        }
    )
    payload = json.loads(text)
    assert payload["citations"][0]["doc_id"] == "OP-BFP-001"
    assert "8.1" in payload["citations"][0]["section"]
    call_filters = mock_retrieve.call_args.kwargs.get("filters") or {}
    assert "asset" not in call_filters
    assert call_filters.get("doc_id") == "OP-BFP-001"


@patch("apps.backend.tools.retrieve_detailed")
def test_search_procedures_retries_when_empty(mock_retrieve):
    empty = RetrievalResult(
        query="q",
        documents=[],
        citations=[],
        scores=[],
        confidence="none",
        reason="none",
    )
    hit_doc = Document(
        page_content="restart criteria",
        metadata={"doc_id": "OP-MTR-003", "section": "7. Restart criteria"},
    )
    hit = RetrievalResult(
        query="q",
        documents=[hit_doc],
        citations=[],
        scores=[0.3],
        confidence="high",
        reason="ok",
    )
    mock_retrieve.side_effect = [empty, empty, hit]
    text = search_procedures.invoke(
        {"query": "motor restart", "site": "EastRefinery", "asset": "Motor M-501"}
    )
    payload = json.loads(text)
    assert payload["confidence"] == "high"
    assert mock_retrieve.call_count == 3
