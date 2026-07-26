# Alarm Investigation and Procedure Guidance Copilot

Senior Software Engineer – Copilot Integration assignment (ABB).

**Selected use case:** Alarm Investigation and Procedure Guidance Copilot

## Main capabilities (target)

- Natural-language alarm investigation
- MCP tools over the Alarm Management API (asset search, alarms, metadata, correlation, priority, recommendations)
- Document RAG over operating procedures, maintenance manuals, troubleshooting guides, and safety instructions
- Combined MCP + RAG answers with citations and MCP execution trace
- Web GUI for chat, alarm summary, citations, and tool traces

## Technology stack (planned)

| Layer | Choice |
|---|---|
| Backend / orchestration | Python (FastAPI) |
| Frontend GUI | React or Streamlit (finalized in implementation) |
| MCP server | Python MCP SDK |
| Alarm API | Supplied `alarm-management-api-simulator` |
| RAG | PDF/Markdown ingestion + vector retrieval |
| Packaging | Docker Compose |
| CI | GitHub Actions |

## Repository layout (ABB guideline)

```text
.
├── README.md
├── docs/
│   ├── architecture.md
│   ├── architecture-diagram.png   # add diagram later
│   ├── mcp-tool-catalog.md
│   ├── rag-design.md
│   ├── api-integration.md
│   ├── design-decisions.md
│   └── known-limitations.md
├── apps/
│   ├── backend/                   # copilot orchestration + MCP client
│   └── frontend/                  # GUI
├── mcp-servers/
│   └── alarm-management/          # candidate-developed MCP server
├── rag/
│   ├── ingestion/
│   ├── retrieval/
│   ├── documents/                 # markdown sources (optional editing)
│   ├── documents-pdf/             # PDF corpus + metadata.json (used for RAG)
│   ├── documents-pdf/             # PDF corpus for PDF extraction demos
│   └── tests/
├── connectors/                    # Alarm API HTTP client, etc.
├── tests/
│   ├── unit/
│   ├── integration/
│   └── e2e/
├── test-data/
├── scripts/
├── .github/workflows/ci.yml
├── .env.example
├── Dockerfile
├── docker-compose.yml
└── Makefile
```

Assignment brief files are also kept in this folder for reference:

- `Assignment_Use_Case.md`
- `Submission_and_Evaluation_Guidelines.md`
- `alarm-management-api-simulator/`

## MCP server

Location: `mcp-servers/alarm-management/`

**Implemented tools** (Step 4):

1. `search_assets` - Find assets by name or ID
2. `get_asset_metadata` - Get detailed asset information
3. `get_alarms` - List alarms with filters
4. `get_recent_critical_alarms` - Quick access to high/critical alarms
5. `correlate_alarms` - Find patterns across assets
6. `calculate_alarm_priority` - Get priority score
7. `get_operator_recommendations` - Get recommended actions

## RAG corpus

- PDF (used for RAG): `rag/documents-pdf/`
- Metadata: `rag/documents-pdf/metadata.json`
- Markdown sources (optional): `rag/documents/`

Ingestion and retrieval code will live under `rag/ingestion/` and `rag/retrieval/`.

## Quick start (current status)

### 1) Alarm API simulator

```bash
cd alarm-management-api-simulator
docker load -i alarm-api-simulator_latest.tar
docker run -d \
  --name alarm-api-simulator \
  --platform linux/amd64 \
  -e AUTH_ENABLED=true \
  -p 8000:8000 \
  alarm-api-simulator-alarm-api-simulator:latest

curl http://localhost:8000/health
curl -H "Authorization: Bearer demo-token" \
  "http://localhost:8000/assets/search?query=Boiler%20Feed%20Pump%20101&limit=5"
```

Swagger: http://localhost:8000/docs

### 2) Copilot stack

Not implemented yet. Later:

```bash
cp .env.example .env
docker compose up --build
```

## Configuration

Copy `.env.example` to `.env`. Do not commit secrets.

## Test commands

```bash
make test
# or later: pytest
```

## Sample interaction (acceptance scenario)

> Investigate recurring high-severity alarms for Boiler Feed Pump 101 over the last 90 days, identify likely contributing factors, retrieve the relevant operating procedure, and provide recommended actions with source evidence.

## Architecture summary

User → GUI → Copilot backend → MCP client → Alarm Management MCP server → Alarm API  
User question also triggers RAG retrieval over procedure/manual PDFs → grounded answer with citations + MCP trace.

See `docs/architecture.md`.

## Assumptions

- Alarm API token for local demo is `demo-token`
- Apple Silicon hosts may need `--platform linux/amd64` (Rosetta) for the supplied simulator image
- Synthetic corpus in `rag/documents*` is representative, not real plant IP

## Known limitations

See `docs/known-limitations.md` (updated as implementation progresses).

## Implementation progress

- [x] Step 1: Alarm API simulator running
- [x] Step 2: ABB repository skeleton + docs placeholders
- [x] Step 3: Alarm API connector/client
- [x] Step 4: MCP server (tools)
- [x] Step 5a: RAG stack (LangChain + OpenAI + Chroma)
- [x] Step 5b–5g: LangChain load → chunk → embed → Chroma index
- [x] Step 5h–5n: filters, citations, grounded answers, injection tests
- [x] Step 6: Copilot backend (MCP client + LangGraph agent)
- [ ] Step 7: GUI
- [ ] Step 8: Tests + CI
- [ ] Step 9: Packaging, demo video, submission
