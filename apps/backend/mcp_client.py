"""In-process FastMCP client for mcp-servers/alarm-management."""
from __future__ import annotations

import asyncio
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

SERVER_DIR = ROOT / "mcp-servers" / "alarm-management"
if str(SERVER_DIR) not in sys.path:
    sys.path.insert(0, str(SERVER_DIR))


def _get_mcp_server():
    import server as alarm_mcp_server

    return alarm_mcp_server.mcp


def _extract_tool_payload(result: Any) -> Any:
    """Normalize FastMCP call_tool result to JSON-serializable data."""
    if result is None:
        return None

    data = getattr(result, "data", None)
    if data is not None:
        return data

    structured = getattr(result, "structured_content", None)
    if structured is not None:
        return structured

    content = getattr(result, "content", None)
    if content:
        texts = []
        for block in content:
            text = getattr(block, "text", None)
            if text is not None:
                texts.append(text)
            elif isinstance(block, dict) and "text" in block:
                texts.append(block["text"])
        if len(texts) == 1:
            try:
                return json.loads(texts[0])
            except json.JSONDecodeError:
                return texts[0]
        if texts:
            return texts

    if isinstance(result, (dict, list, str, int, float, bool)):
        return result
    return str(result)


async def _list_tools_async() -> list[dict]:
    from fastmcp import Client

    mcp = _get_mcp_server()
    async with Client(mcp) as client:
        tools = await client.list_tools()
        out = []
        for t in tools:
            out.append(
                {
                    "name": getattr(t, "name", None) or t.get("name"),
                    "description": getattr(t, "description", None)
                    or (t.get("description") if isinstance(t, dict) else ""),
                }
            )
        return out


async def _call_tool_async(name: str, arguments: dict | None = None) -> Any:
    from fastmcp import Client

    mcp = _get_mcp_server()
    async with Client(mcp) as client:
        result = await client.call_tool(name, arguments or {})
        return _extract_tool_payload(result)


def list_mcp_tools() -> list[dict]:
    """Discover tools exposed by the alarm-management MCP server."""
    return asyncio.run(_list_tools_async())


def call_mcp_tool(name: str, arguments: dict | None = None) -> Any:
    """Invoke one MCP tool by name (sync wrapper)."""
    try:
        return asyncio.run(_call_tool_async(name, arguments or {}))
    except Exception as exc:
        return {
            "error": True,
            "tool": name,
            "message": str(exc),
            "type": type(exc).__name__,
        }


def call_mcp_tool_json(name: str, arguments: dict | None = None) -> str:
    """Invoke MCP tool and return a JSON string for LLM tool results."""
    payload = call_mcp_tool(name, arguments)
    return json.dumps(payload, default=str)
