# Architecture

## Overview

This copilot answers alarm investigation questions by combining two sources in one run:

1. Live data from the Alarm Management API (through MCP)
2. Procedure / manual text from a local RAG index

GUI is Streamlit. Orchestration is a LangGraph ReAct agent in `apps/backend`.

## Diagram

![Architecture diagram](architecture-diagram.png)

Left/blue side is the MCP path (GUI → agent → MCP client → MCP server → Alarm API).  
Green side is RAG (`search_procedures` → Chroma / PDFs → citations).

## Main pieces

| Piece | Where | Notes |
|---|---|---|
| GUI | `apps/frontend` | Chat, alarm list, citations, tool trace expanders |
| Agent | `apps/backend` | Decides which tools to call and writes the final answer |
| MCP client | `apps/backend/mcp_client.py` | Discovers and calls MCP tools (in-process FastMCP client for local demos) |
| MCP server | `mcp-servers/alarm-management` | Thin tools over the Alarm API |
| Connector | `connectors/alarm_api` | httpx client: auth, retries, timeouts, error mapping |
| Alarm API | Docker simulator on `:8000` | Assets, alarms, priority, recommendations, etc. |
| Ingest | `rag/ingestion` | PDF load → chunk → embed → Chroma |
| Retrieval | `rag/retrieval` | Filtered search + citations |
| Secrets | `.env` | API token and OpenAI key stay out of the UI |

## Typical request

1. User asks something in Streamlit.
2. Agent gets MCP tools + `search_procedures`.
3. Common tool sequence for an investigation:
   - `search_assets` to get `asset_id`
   - `get_recent_critical_alarms` (or `get_alarms`)
   - maybe one `get_operator_recommendations` call
   - `search_procedures` for OP / SI / TG text
4. Tool outputs stay in the agent message list.
5. Model writes the answer with section citations.
6. GUI shows answer, alarms, citations, and the raw-ish tool trace.

## Rules I stuck to

- Backend agent never imports the Alarm API client for live calls. Only MCP → connector does that.
- Retrieved doc text is treated as data, not instructions (injection fixture is excluded from normal search).
- Bearer token is not printed in GUI traces.

## Persistence

Chroma index lives under `VECTOR_STORE_URL` (default `./rag/.index`).  
There is no chat database. Chat history in the UI is for display; each investigation starts a new agent run.
