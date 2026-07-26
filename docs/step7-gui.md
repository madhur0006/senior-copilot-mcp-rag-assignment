# Step 7 — GUI (Streamlit)

## Run

```bash
# prereqs
docker start alarm-api-simulator
# RAG index already built once:
# PYTHONPATH=. python3 -m rag.ingestion.pipeline

source .venv/bin/activate
pip install streamlit   # if needed
PYTHONPATH=. streamlit run apps/frontend/app.py
```

Opens a local browser UI (default http://localhost:8501).

## Panels

| Area | Content |
|------|---------|
| Chat | Natural-language investigation |
| Alarm summary | Parsed from MCP `get_alarms` / `get_recent_critical_alarms` |
| Document citations | From RAG `search_procedures` |
| MCP tool trace | Expandable request args + response preview |
| Errors | Shown if investigation fails |

Sample query button loads the assignment BFP-101 investigation prompt.
