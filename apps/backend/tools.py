"""
LangChain tools for the copilot.

- Alarm tools go through the MCP client (same catalog as mcp-servers/alarm-management)
- RAG tool uses retrieve_detailed (local Chroma index)
"""
from __future__ import annotations

import json
from langchain_core.tools import tool

from apps.backend.mcp_client import call_mcp_tool_json
from rag.retrieval.retriever import retrieve_detailed


def _dump(payload) -> str:
    return json.dumps(payload, default=str)


@tool
def search_assets(
    query: str,
    site: str = "",
    unit: str = "",
    limit: int = 25,
) -> str:
    """Search for plant assets by name or ID via MCP (e.g. 'Boiler Feed Pump 101')."""
    args = {"query": query, "limit": limit}
    if site:
        args["site"] = site
    if unit:
        args["unit"] = unit
    return call_mcp_tool_json("search_assets", args)


@tool
def get_asset_metadata(asset_id: str) -> str:
    """Get detailed metadata for an asset ID (e.g. AST00001) via MCP."""
    return call_mcp_tool_json("get_asset_metadata", {"asset_id": asset_id})


@tool
def get_alarms(
    asset_id: str = "",
    severity: str = "",
    status: str = "",
    page: int = 1,
    page_size: int = 25,
) -> str:
    """List alarms via MCP. Optional filters: asset_id, severity (low/medium/high/critical), status."""
    args: dict = {"page": page, "page_size": page_size}
    if asset_id:
        args["asset_id"] = asset_id
    if severity:
        args["severity"] = severity
    if status:
        args["status"] = status
    return call_mcp_tool_json("get_alarms", args)


@tool
def get_recent_critical_alarms(asset_id: str, days: int = 90) -> str:
    """Get recent high/critical alarms for an asset over the last N days via MCP."""
    return call_mcp_tool_json(
        "get_recent_critical_alarms",
        {"asset_id": asset_id, "days": days},
    )


@tool
def correlate_alarms(asset_ids: str, days: int = 90) -> str:
    """
    Correlate alarms across assets via MCP.
    Pass asset_ids as a comma-separated string, e.g. 'AST00001,AST00002'.
    """
    ids = [a.strip() for a in asset_ids.split(",") if a.strip()]
    return call_mcp_tool_json("correlate_alarms", {"asset_ids": ids, "days": days})


@tool
def calculate_alarm_priority(alarm_id: str) -> str:
    """Calculate priority score for one alarm via MCP."""
    return call_mcp_tool_json("calculate_alarm_priority", {"alarm_id": alarm_id})


@tool
def get_operator_recommendations(alarm_id: str) -> str:
    """Get API operator recommendations for an alarm via MCP."""
    return call_mcp_tool_json("get_operator_recommendations", {"alarm_id": alarm_id})


@tool
def search_procedures(
    query: str,
    site: str = "EastRefinery",
    asset: str = "",
    doc_type: str = "",
    k: int = 4,
) -> str:
    """
    Retrieve relevant operating procedures / manuals / guides from the RAG index.
    Returns excerpts with doc_id, section, source_path, and distance scores.
    Use this after you know the asset/alarm context so you can ground the answer.
    """
    filters: dict = {}
    if site:
        filters["site"] = site
    if asset:
        filters["asset"] = asset
    if doc_type:
        filters["doc_type"] = doc_type

    result = retrieve_detailed(
        query=query,
        k=k,
        filters=filters or None,
    )
    payload = {
        "confidence": result.confidence,
        "reason": result.reason,
        "citations": [c.to_dict() for c in result.citations],
        "excerpts": [
            {
                "doc_id": (d.metadata or {}).get("doc_id"),
                "section": (d.metadata or {}).get("section"),
                "text": (d.page_content or "")[:1200],
            }
            for d in result.documents
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
