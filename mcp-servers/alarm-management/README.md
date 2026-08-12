# Alarm Management MCP server

Thin MCP wrapper over the Alarm Management API.

## Tools

| Tool | Purpose |
|------|---------|
| `search_assets` | Search assets |
| `get_asset_metadata` | Asset details |
| `get_alarms` | List / filter alarms |
| `get_recent_critical_alarms` | High/critical over N days |
| `correlate_alarms` | Correlation across assets |
| `calculate_alarm_priority` | Priority score |
| `get_operator_recommendations` | Recommended actions |

## Run

```bash
cd mcp-servers/alarm-management
PYTHONPATH=../.. python3 server.py
```

Needs the Alarm API up (`ALARM_API_BASE_URL`, default `http://localhost:8000`) and `ALARM_API_TOKEN`.

## Used by the copilot

`apps/backend/mcp_client.py` loads this server and calls the tools during an investigation. Procedure text comes from the separate RAG tool `search_procedures`.
