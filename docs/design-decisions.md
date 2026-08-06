# Design decisions

Short notes on why things are wired the way they are.

## Choices

1. **Repo layout** – Followed the ABB suggested folders (`apps/`, `mcp-servers/`, `rag/`, `connectors/`, `docs/`, `tests/`).
2. **GUI** – Streamlit. Enough for chat + side panels + expandable traces without building a separate React app in the time box.
3. **Agent** – Explicit LangGraph graph with `agent` and `tools` nodes. Easier to follow than a fully hidden helper when explaining MCP + RAG chaining.
4. **MCP** – FastMCP. Copilot uses an in-process client against the same `server.py` for local demos; tools are still discovered/called as MCP tools.
5. **Alarm API** – Only reached from the MCP server through `connectors/alarm_api` (auth, retry, timeout, error mapping).
6. **LLM** – OpenAI only (`gpt-4o-mini` + `text-embedding-3-small`). Kept one provider to reduce setup pain.
7. **Vector store** – Local Chroma with `PersistentClient`. Early on LangChain tried HttpClient on `:8000`, which collided with the Alarm API simulator, so the client is created explicitly.
8. **Docs** – Edit Markdown under `rag/documents/`; ingest PDFs from `rag/documents-pdf/`.
9. **Context size** – Tool results are compacted before they go back to the model. Full alarm dumps were blowing the context window.
10. **Simulator image** – Large `.tar` is gitignored. Compose starts the API; GUI/MCP are started with Make / `PYTHONPATH`.

## Things I considered and skipped

| Idea | Why not |
|---|---|
| FastAPI + React UI | More moving parts for little demo gain |
| HTTP-only MCP process for every local run | Extra process to manage; in-process client was enough for the assignment demo |
| Google + OpenAI embeddings | Two providers, more config |
| Hosted vector DB | Extra account/dependency for reviewers |

## Security / safety notes

- `.env` is ignored; `.env.example` has placeholders.
- `TEST-INJECT-999` is kept out of normal retrieval; prompts say retrieved text is untrusted.
- No ticket/write tools are hooked up for unsupervised writes.
