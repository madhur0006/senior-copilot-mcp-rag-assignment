"""
Copilot service — run an end-to-end investigation with tool trace.
"""
from __future__ import annotations

import json
from typing import Any

from langchain_core.messages import AIMessage, HumanMessage, ToolMessage

from apps.backend.agent import build_agent
from apps.backend.mcp_client import list_mcp_tools
from apps.backend.models import InvestigationResult, ToolTraceItem
from rag.ingestion.config import RagConfig


def _preview(value: Any, limit: int = 500) -> str:
    text = value if isinstance(value, str) else json.dumps(value, default=str)
    text = text.replace("\n", " ")
    return text[:limit] + ("..." if len(text) > limit else "")


def _extract_trace(messages: list) -> tuple[list[ToolTraceItem], list[dict]]:
    """Build a tool trace and collect RAG citations from full tool messages."""
    pending_calls: dict[str, ToolTraceItem] = {}
    trace: list[ToolTraceItem] = []
    citations: list[dict] = []

    for msg in messages:
        if isinstance(msg, AIMessage) and getattr(msg, "tool_calls", None):
            for call in msg.tool_calls:
                call_id = call.get("id") or ""
                item = ToolTraceItem(
                    tool=call.get("name") or "unknown",
                    arguments=call.get("args") or {},
                )
                if call_id:
                    pending_calls[call_id] = item
                trace.append(item)

        elif isinstance(msg, ToolMessage):
            call_id = getattr(msg, "tool_call_id", "") or ""
            item = pending_calls.get(call_id)
            content = msg.content
            if isinstance(content, list):
                content = json.dumps(content, default=str)
            content_str = str(content)
            preview = _preview(content_str)
            ok = not (
                '"error": true' in content_str.lower()
                or content_str.strip().startswith("Error")
            )
            tool_name = getattr(msg, "name", None) or (item.tool if item else "tool")

            if item is None:
                item = ToolTraceItem(tool=tool_name, result_preview=preview, ok=ok)
                trace.append(item)
            else:
                item.result_preview = preview
                item.ok = ok

            if tool_name == "search_procedures":
                try:
                    data = json.loads(content_str)
                    for cite in data.get("citations") or []:
                        if cite not in citations:
                            citations.append(cite)
                except Exception:
                    pass

    return trace, citations


def _final_answer(messages: list) -> str:
    for msg in reversed(messages):
        if isinstance(msg, AIMessage) and msg.content and not msg.tool_calls:
            content = msg.content
            if isinstance(content, list):
                parts = []
                for block in content:
                    if isinstance(block, str):
                        parts.append(block)
                    elif isinstance(block, dict) and "text" in block:
                        parts.append(block["text"])
                return "\n".join(parts).strip()
            return str(content).strip()
    return "No final answer was produced."


def run_investigation(
    query: str,
    config: RagConfig = None,
    discover_tools: bool = True,
) -> InvestigationResult:
    """
    Run the LangGraph MCP+RAG agent for one natural-language investigation request.
    """
    if config is None:
        config = RagConfig()

    discovered: list[str] = []
    if discover_tools:
        try:
            discovered = [t["name"] for t in list_mcp_tools() if t.get("name")]
        except Exception as exc:
            discovered = [f"(discovery failed: {exc})"]

    agent = build_agent(config)
    result = agent.invoke({"messages": [HumanMessage(content=query)]})
    messages = result.get("messages") or []

    trace, citations = _extract_trace(messages)

    return InvestigationResult(
        query=query,
        answer=_final_answer(messages),
        tool_trace=trace,
        citations=citations,
        mcp_tools_discovered=discovered,
    )
