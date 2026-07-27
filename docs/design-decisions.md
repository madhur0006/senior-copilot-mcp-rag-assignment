# Design Decisions

## Locked choices

1. **Repository layout** — Follow ABB recommended structure (`apps/`, `mcp-servers/`, `rag/`, `connectors/`, `docs/`, `tests/`).
2. **Frontend** — Streamlit for a fast, assignment-ready GUI (chat + panels + expandable traces).
3. **Orchestration** — Explicit LangGraph ReAct graph (`agent` ↔ `tools`) instead of a black-box agent helper, for clearer MCP+RAG tool chaining.
4. **MCP framework** — FastMCP server; in-process FastMCP Client for local reliability (same tool catalog as standalone `server.py`).
5. **Alarm API access** — Only through MCP → `connectors/alarm_api` (auth, retries, timeouts, error mapping). Orchestration never imports the HTTP client for live calls.
6. **LLM / embeddings** — OpenAI only (`gpt-4o-mini`, `text-embedding-3-small`) via LangChain.
7. **Vector store** — Local Chroma with explicit `PersistentClient` (avoids HttpClient colliding with Alarm API on `:8000`).
8. **Corpus** — Markdown under `rag/documents/` for editing; PDFs under `rag/documents-pdf/` are what ingestion reads.
9. **Tool output size** — Compact MCP/RAG tool JSON before returning to the LLM to stay under context limits.
10. **Simulator packaging** — Large `*.tar` gitignored; load once locally. Compose starts Alarm API; GUI/MCP run via Makefile / PYTHONPATH.

## Alternatives considered

| Topic | Not chosen | Why |
|---|---|---|
| FastAPI + React GUI | Extra surface for the time box | Streamlit covers chat/trace/citations quickly |
| HTTP MCP transport only | More moving parts locally | In-process client still uses real MCP list/call protocol |
| Google embeddings | Dual-provider complexity | Single OpenAI provider simplifies ops and CI |
| Cloud vector DB | External dependency | Local Chroma is reproducible for evaluators |

## Security notes

- `.env` is gitignored; `.env.example` has placeholders only.
- Prompt-injection fixture `TEST-INJECT-999` is excluded from normal retrieval; grounded prompts treat excerpts as data.
- No write/ticket tools are exposed without confirmation (ticketing URL is placeholder only).
