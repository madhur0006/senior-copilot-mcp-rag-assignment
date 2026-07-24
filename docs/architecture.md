# Architecture

## Use case

Alarm Investigation and Procedure Guidance Copilot.

## High-level components

1. **GUI** (`apps/frontend`) — chat, alarm summary, citations, MCP trace
2. **Copilot orchestration** (`apps/backend`) — intent/planning, tool chaining, answer assembly
3. **MCP client** (inside backend) — tool discovery and invocation
4. **MCP server** (`mcp-servers/alarm-management`) — typed tools over Alarm API
5. **Alarm Management API** (simulator or equivalent)
6. **RAG ingestion** (`rag/ingestion`) — PDF/MD extract, chunk, embed, index
7. **RAG retrieval** (`rag/retrieval`) — filtered search + citations
8. **Connectors** (`connectors`) — HTTP clients, auth, retries, tracing
9. **Observability** — request/conversation/trace IDs, tool timings, retrieval scores
10. **Auth boundaries** — API token only inside MCP/connectors; never exposed in GUI responses

## Request flow (target)

1. User asks a natural-language question in the GUI.
2. Backend plans steps and discovers MCP tools.
3. MCP tools resolve asset → alarms → metadata → correlation/priority → recommendations.
4. Backend retrieves procedure/manual passages via RAG.
5. Backend compares API recommendations with document guidance.
6. GUI shows grounded answer, citations, and expandable MCP trace.

## Diagram

Add `docs/architecture-diagram.png` in a later step showing MCP and RAG paths explicitly.
