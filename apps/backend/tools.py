"""
LangChain tools for the copilot.

- Alarm tools go through the MCP client (same catalog as mcp-servers/alarm-management)
- RAG tool uses retrieve_detailed (local Chroma index)

Tool outputs are compacted so LangGraph message history stays under model context limits.
"""
from __future__ import annotations

import json
import re

from langchain_core.tools import tool

from apps.backend.mcp_client import call_mcp_tool
from rag.retrieval.retriever import retrieve_detailed

# Keep tool messages small — full alarm dumps overflow gpt-4o-mini context
_MAX_TOOL_CHARS = 6000
_ALARM_KEYS = (
    "alarm_id",
    "asset_id",
    "asset_name",
    "alarm_name",
    "alarm_code",
    "alarm_message",
    "severity",
    "priority",
    "status",
    "start_time",
    "end_time",
    "duration_minutes",
    "operator_action",
)


def _dump(payload, max_chars: int = _MAX_TOOL_CHARS) -> str:
    text = json.dumps(payload, default=str)
    if len(text) <= max_chars:
        return text
    return text[: max_chars - 24] + '..."[truncated]"}'


def _compact_alarm_row(row: dict) -> dict:
    return {k: row.get(k) for k in _ALARM_KEYS if row.get(k) is not None}


def _compact_alarm_payload(payload, limit: int = 8) -> dict:
    if not isinstance(payload, dict):
        return {"raw": str(payload)[:2000]}
    if payload.get("error"):
        return payload
    items = (
        payload.get("data")
        or payload.get("items")
        or payload.get("alarms")
        or payload.get("results")
        or []
    )
    if not isinstance(items, list):
        return {"summary": str(payload)[:2000]}
    compact = [_compact_alarm_row(r) for r in items[:limit] if isinstance(r, dict)]
    return {
        "count_returned": len(compact),
        "count_total_estimate": len(items),
        "alarms": compact,
        "note": "Compacted for context limits; showing most recent subset.",
    }


@tool
def search_assets(
    query: str,
    site: str = "",
    unit: str = "",
    limit: int = 5,
) -> str:
    """Search for plant assets by name or ID via MCP (e.g. 'Boiler Feed Pump 101')."""
    args = {"query": query, "limit": min(limit, 10)}
    if site:
        args["site"] = site
    if unit:
        args["unit"] = unit
    return _dump(call_mcp_tool("search_assets", args))


@tool
def get_asset_metadata(asset_id: str) -> str:
    """Get detailed metadata for an asset ID (e.g. AST00001) via MCP."""
    return _dump(call_mcp_tool("get_asset_metadata", {"asset_id": asset_id}))


@tool
def get_alarms(
    asset_id: str = "",
    severity: str = "",
    status: str = "",
    page: int = 1,
    page_size: int = 10,
) -> str:
    """List alarms via MCP. Optional filters: asset_id, severity (low/medium/high/critical), status."""
    args: dict = {"page": page, "page_size": min(page_size, 15)}
    if asset_id:
        args["asset_id"] = asset_id
    if severity:
        args["severity"] = severity
    if status:
        args["status"] = status
    return _dump(_compact_alarm_payload(call_mcp_tool("get_alarms", args), limit=10))


@tool
def get_recent_critical_alarms(asset_id: str, days: int = 90) -> str:
    """Get recent high/critical alarms for an asset over the last N days via MCP."""
    payload = call_mcp_tool(
        "get_recent_critical_alarms",
        {"asset_id": asset_id, "days": days},
    )
    return _dump(_compact_alarm_payload(payload, limit=8))


@tool
def correlate_alarms(asset_ids: str, days: int = 90) -> str:
    """
    Correlate alarms across assets via MCP.
    Pass asset_ids as a comma-separated string, e.g. 'AST00001,AST00002'.
    """
    ids = [a.strip() for a in asset_ids.split(",") if a.strip()][:5]
    return _dump(call_mcp_tool("correlate_alarms", {"asset_ids": ids, "days": days}))


@tool
def calculate_alarm_priority(alarm_id: str) -> str:
    """Calculate priority score for one alarm via MCP."""
    return _dump(call_mcp_tool("calculate_alarm_priority", {"alarm_id": alarm_id}))


@tool
def get_operator_recommendations(alarm_id: str) -> str:
    """Get API operator recommendations for an alarm via MCP. Use at most 1–2 times."""
    return _dump(call_mcp_tool("get_operator_recommendations", {"alarm_id": alarm_id}))


@tool
def search_procedures(
    query: str,
    site: str = "EastRefinery",
    asset: str = "",
    doc_type: str = "",
    doc_id: str = "",
    k: int = 3,
) -> str:
    """
    Retrieve relevant operating procedures / manuals / guides from the RAG index.
    Returns excerpts with doc_id, section, source_path, and distance scores.

    Tips:
    - Prefer symptom-specific queries (e.g. 'motor trip restart criteria').
    - Use equipment names for asset (e.g. 'Motor M-501'), NEVER Alarm API ids like AST00001.
    - If the user names a document (e.g. OP-MTR-003), set doc_id to that value.
    """

    def _run(filters: dict | None):
        result = retrieve_detailed(
            query=query,
            k=max(k + 4, 8),
            filters=filters or None,
        )
        pairs = list(zip(result.documents, result.scores))
        preferred = [
            (d, s)
            for d, s in pairs
            if str((d.metadata or {}).get("section") or "").strip().lower()
            not in {"", "introduction", "full document"}
        ]
        chosen = (preferred or pairs)[:k]
        docs = [d for d, _ in chosen]
        scores = [s for _, s in chosen]
        from rag.retrieval.citations import citations_from_hits

        citations = citations_from_hits(list(zip(docs, scores)))
        return result, docs, citations

    filters: dict = {}
    if doc_id:
        filters["doc_id"] = doc_id.strip()
    if site:
        filters["site"] = site
    if doc_type:
        filters["doc_type"] = doc_type

    # Alarm API asset ids (AST00001) are NOT in document metadata — skip them
    asset_clean = (asset or "").strip()
    if asset_clean and not re.fullmatch(r"AST\d+", asset_clean, flags=re.I):
        filters["asset"] = asset_clean

    result, docs, citations = _run(filters or None)

    # Retry without asset/site if nothing useful (common when agent passes AST ids)
    if not docs:
        loose = {}
        if doc_id:
            loose["doc_id"] = doc_id.strip()
        if doc_type:
            loose["doc_type"] = doc_type
        result, docs, citations = _run(loose or None)

    if not docs and (doc_id or asset_clean or site):
        result, docs, citations = _run(None)

    payload = {
        "confidence": result.confidence if docs else "none",
        "reason": result.reason if docs else "No matching procedure chunks for this query/filters.",
        "citations": [c.to_dict() for c in citations],
        "excerpts": [
            {
                "doc_id": (d.metadata or {}).get("doc_id"),
                "section": (d.metadata or {}).get("section"),
                "text": (d.page_content or "")[:700],
            }
            for d in docs
        ],
    }
    return _dump(payload)


COPILOT_TOOLS = [
    search_assets,
    get_asset_metadata,
    get_alarms,
    get_recent_critical_alarms,
    correlate_alarms,
    calculate_alarm_priority,
    get_operator_recommendations,
    search_procedures,
]
