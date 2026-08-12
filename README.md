# Alarm Investigation and Procedure Guidance Copilot Using MCP and RAG

ABB Senior Software Engineer – Copilot Integration assignment.

Use case: investigate plant alarms with live API data (MCP) and procedure docs (RAG), then show the answer in a small Streamlit UI.

## What it does

- Take a natural language question (e.g. BFP-101 high severity alarms over 90 days)
- Call Alarm Management API tools through an MCP server (not direct HTTP from the agent)
- Pull matching procedure / safety / troubleshooting text from a local RAG index
- Return an answer with citations plus an expandable MCP tool trace in the GUI

## Stack

| Layer | What I used |
|---|---|
| Agent | Python + LangGraph (ReAct loop) |
| GUI | Streamlit |
| MCP | FastMCP under `mcp-servers/alarm-management` |
| Alarm API | Provided simulator |
| RAG | LangChain, OpenAI embeddings, Chroma on disk |
| Chat model | `gpt-4o-mini` |
| CI | GitHub Actions + pytest |

## MCP tools

Code: `mcp-servers/alarm-management/`

| Tool | Purpose |
|---|---|
| `search_assets` | Name / ID → asset |
| `get_asset_metadata` | Metadata + related assets |
| `get_alarms` | Filtered alarm list |
| `get_recent_critical_alarms` | High/critical over N days |
| `correlate_alarms` | Simple co-occurrence across assets |
| `calculate_alarm_priority` | Priority score |
| `get_operator_recommendations` | API recommended actions |

Details and schemas: [docs/mcp-tool-catalog.md](docs/mcp-tool-catalog.md)

Standalone server:

```bash
make simulator-up
cd mcp-servers/alarm-management
PYTHONPATH=../.. python3 server.py
```

For the GUI demo the backend talks to the same server module in-process (`apps/backend/mcp_client.py`). That still goes through the MCP client/tool protocol; it just avoids standing up a separate port for local runs.

## RAG

- PDFs used at ingest time: `rag/documents-pdf/` + `metadata.json`
- Markdown copies for editing: `rag/documents/`
- Index path: `rag/.index` (not committed; rebuild locally)
- Embedding model: `text-embedding-3-small`

```bash
PYTHONPATH=. python3 -m rag.ingestion.pipeline
```

More detail: [docs/rag-design.md](docs/rag-design.md)

## Quick start

```bash
cp .env.example .env
# set OPENAI_API_KEY (and LLM_API_KEY if you use that alias)

cd alarm-management-api-simulator
docker load -i alarm-api-simulator_latest.tar   # first time
cd ..
make simulator-up

python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
make ingest

PYTHONPATH=. streamlit run apps/frontend/app.py
```

Checks:

- API health: `curl http://localhost:8000/health`
- Swagger: http://localhost:8000/docs

Optional CLI run: `make investigate`

## Config

Put secrets only in `.env` (gitignored). Main variables:

| Variable | Notes |
|---|---|
| `ALARM_API_BASE_URL` | default `http://localhost:8000` |
| `ALARM_API_TOKEN` | simulator uses `demo-token` |
| `OPENAI_API_KEY` / `LLM_API_KEY` | needed for embed + chat |
| `DOCUMENT_PDF_PATH` | PDF root |
| `VECTOR_STORE_URL` | Chroma path |

## Make targets

```bash
make simulator-up
make simulator-down
make ingest
make investigate
make test
make coverage
```

`docker compose up -d` starts the Alarm API simulator. MCP and Streamlit are started from Make / `PYTHONPATH` for the local demo (see Quick start).

## Tests

```bash
make test-unit
make test
make coverage   # HTML under coverage/html/
```

Covered today:

- Unit tests for connector, MCP tools, RAG chunk/retrieve/grounding, and agent helpers
- Integration tests against the live simulator / index when available
- E2E investigation test combining MCP + RAG (mocked path runs in CI)

CI (GitHub Actions) runs unit tests + the mocked MCP+RAG e2e on every push/PR and uploads coverage XML/HTML.

## Example questions

MCP + RAG:

> Investigate recurring high-severity alarms for Boiler Feed Pump 101 over the last 90 days. Summarize the top alarms, then give recommended operator actions from OP-BFP-001 / SI-BFP-031 with section citations.

RAG only:

> What does OP-MTR-003 say about when restart is allowed after a motor trip? Cite the section.

Another MCP + RAG case:

> Why are high discharge-pressure alarms recurring on the centrifugal compressor? Pull recent critical alarms via MCP and recommend actions from TG-CMP-021 / OP-CMP-002 with section citations.

## Architecture

```text
User → Streamlit → LangGraph agent
         ├─ MCP client → MCP server → Alarm API
         └─ search_procedures → Chroma / PDFs
       → answer + citations + tool trace
```

- Diagram: [docs/architecture-diagram.png](docs/architecture-diagram.png)
- Notes: [docs/architecture.md](docs/architecture.md)

## Runtime notes

- Simulator auth token: `demo-token` (when `AUTH_ENABLED=true`)
- Apple Silicon: `make simulator-up` already uses `--platform linux/amd64`
- `rag/documents*` are sample EastRefinery docs written for this assignment (not real plant IP)
- Local run model: Compose = Alarm API; MCP + Streamlit via Make / `PYTHONPATH` (see [docs/known-limitations.md](docs/known-limitations.md))

## Demo

- Video: [video-explanation/abb-alarm-api-mcp-video.mp4](video-explanation/abb-alarm-api-mcp-video.mp4)
- Architecture diagram: [docs/architecture-diagram.png](docs/architecture-diagram.png)

## Layout

```text
apps/backend/                 agent, MCP client, tools
apps/frontend/                Streamlit UI
mcp-servers/alarm-management/ MCP server
rag/                          ingest, retrieval, PDFs
connectors/alarm_api/         HTTP client used by MCP
tests/                        unit, integration, e2e
docs/                         architecture, MCP catalog, RAG notes
```
