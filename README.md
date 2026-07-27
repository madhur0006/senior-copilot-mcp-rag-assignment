# Alarm Investigation and Procedure Guidance Copilot

Senior Software Engineer – Copilot Integration assignment (ABB).

**Selected use case:** Alarm Investigation and Procedure Guidance Copilot

## Main capabilities

- Natural-language alarm investigation
- MCP tools over the Alarm Management API (asset search, alarms, metadata, correlation, priority, recommendations)
- Document RAG over operating procedures, maintenance manuals, troubleshooting guides, and safety instructions
- Combined MCP + RAG answers with citations and MCP execution trace
- Streamlit GUI for chat, alarm summary, citations, and expandable tool traces

## Technology stack

| Layer | Choice |
|---|---|
| Orchestration | Python, LangGraph ReAct agent |
| Frontend GUI | Streamlit |
| MCP server | FastMCP (`mcp-servers/alarm-management`) |
| Alarm API | Supplied `alarm-management-api-simulator` |
| RAG | LangChain + OpenAI embeddings + Chroma |
| LLM | OpenAI `gpt-4o-mini` |
| Packaging | Docker Compose (Alarm API) + Makefile local run |
| CI | GitHub Actions |

## MCP server

Location: `mcp-servers/alarm-management/`

| Tool | Purpose |
|---|---|
| `search_assets` | Resolve asset name / ID |
| `get_asset_metadata` | Asset details and related assets |
| `get_alarms` | List alarms with filters |
| `get_recent_critical_alarms` | High/critical alarms over N days |
| `correlate_alarms` | Co-occurrence across assets |
| `calculate_alarm_priority` | Priority score for one alarm |
| `get_operator_recommendations` | API operator actions |

Full contracts: [`docs/mcp-tool-catalog.md`](docs/mcp-tool-catalog.md)

### Start MCP server independently

```bash
# Alarm API must be running first
make simulator-up

cd mcp-servers/alarm-management
PYTHONPATH=../.. python3 server.py
```

The copilot uses an in-process FastMCP client (`apps/backend/mcp_client.py`) against the same server module — no separate HTTP port required for local demos.

## RAG corpus and ingestion

- PDF corpus (ingested): `rag/documents-pdf/` + `metadata.json`
- Markdown sources (editing only): `rag/documents/`
- Index: `rag/.index` (Chroma; gitignored — rebuild locally)
- Embeddings: `text-embedding-3-small`
- Retrieval: filtered similarity search with citations and low-confidence handling

```bash
PYTHONPATH=. python3 -m rag.ingestion.pipeline
```

Details: [`docs/rag-design.md`](docs/rag-design.md)

## Quick start

### 1) Configure environment

```bash
cp .env.example .env
# Set OPENAI_API_KEY (and LLM_API_KEY) in .env
```

### 2) Alarm API simulator

```bash
cd alarm-management-api-simulator
docker load -i alarm-api-simulator_latest.tar   # first time only
cd ..
make simulator-up
```

Health check: `curl http://localhost:8000/health`  
Swagger: http://localhost:8000/docs

### 3) Build RAG index

```bash
source .venv/bin/activate   # or: python3 -m venv .venv && pip install -r requirements.txt
PYTHONPATH=. python3 -m rag.ingestion.pipeline
```

### 4) Run GUI

```bash
PYTHONPATH=. streamlit run apps/frontend/app.py
```

### 5) CLI investigation (optional)

```bash
make investigate
# or: PYTHONPATH=. python3 -m apps.backend
```

## Configuration

Copy `.env.example` to `.env`. Do not commit secrets.

| Variable | Purpose |
|---|---|
| `ALARM_API_BASE_URL` | Alarm API base (default `http://localhost:8000`) |
| `ALARM_API_TOKEN` | Bearer token (simulator: `demo-token`) |
| `OPENAI_API_KEY` / `LLM_API_KEY` | OpenAI key for embed + chat |
| `DOCUMENT_PDF_PATH` | PDF corpus root |
| `VECTOR_STORE_URL` | Chroma index path |

## Build and run commands

```bash
make env              # create .env from example if missing
make simulator-up     # start Alarm API container
make simulator-down   # stop Alarm API
make ingest           # build RAG index
make retrieve         # sample grounded RAG answer
make investigate      # full MCP+RAG CLI run
make test             # unit + integration + e2e
make coverage         # coverage HTML/XML under coverage/
```

Compose (Alarm API only today):

```bash
docker compose up -d
```

## Test commands

```bash
make test          # unit + integration + e2e (live tests skip if API/index/key missing)
make test-unit
make test-e2e
make coverage      # unit + mocked e2e → coverage/html + coverage/coverage.xml
```

Coverage HTML: open `coverage/html/index.html` after `make coverage` (typically ~70%+ with GUI/CLI omitted via `.coveragerc`).  
CI uploads the same reports as a GitHub Actions artifact on every push/PR.

## Sample interactions

**Acceptance scenario (MCP + RAG):**

> Investigate recurring high-severity alarms for Boiler Feed Pump 101 over the last 90 days. Summarize the top alarms, then give recommended operator actions from OP-BFP-001 / SI-BFP-031 with section citations.

**RAG-focused:**

> What does OP-MTR-003 say about when restart is allowed after a motor trip? Cite the section.

**Compressor (MCP + RAG):**

> Why are high discharge-pressure alarms recurring on the centrifugal compressor? Pull recent critical alarms via MCP and recommend actions from TG-CMP-021 / OP-CMP-002 with section citations.

## Architecture summary

```text
User → Streamlit GUI → LangGraph agent
         ├─ MCP client → Alarm MCP server → Alarm API
         └─ search_procedures (RAG) → Chroma / procedure PDFs
       → Grounded answer + citations + MCP tool trace
```

- Diagram: [`docs/architecture-diagram.png`](docs/architecture-diagram.png)
- Write-up: [`docs/architecture.md`](docs/architecture.md)

## Assumptions

- Local Alarm API token is `demo-token` when `AUTH_ENABLED=true`
- Apple Silicon may need `--platform linux/amd64` for the supplied simulator image
- Corpus under `rag/documents*` is synthetic / representative, not real plant IP
- OpenAI API access is available for embeddings and chat

## Known limitations

See [`docs/known-limitations.md`](docs/known-limitations.md).

Highlights: full multi-service Compose packaging is not wired yet; demo video/screenshots still outstanding for final submission.

## Demo evidence

- Demo video (≤10 min): _link to be added_
- Screenshots: _to be added under `docs/` or linked from README_

## Repository layout

```text
.
├── apps/backend/          # LangGraph agent + MCP client + RAG tools
├── apps/frontend/         # Streamlit GUI
├── mcp-servers/alarm-management/
├── rag/ingestion|retrieval|documents-pdf/
├── connectors/alarm_api/
├── tests/unit|integration|e2e/
├── docs/                  # architecture, MCP catalog, RAG design, …
├── .env.example
├── docker-compose.yml
└── Makefile
```
