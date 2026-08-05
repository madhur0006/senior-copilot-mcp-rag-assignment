# Alarm Management MCP Server

Exposes Alarm Management API capabilities as MCP tools.

## Tools

| Tool | Purpose |
|------|---------|
| `search_assets` | Find assets by name or ID |
| `get_asset_metadata` | Asset details and related assets |
| `get_alarms` | List alarms with filters |
| `get_recent_critical_alarms` | High/critical alarms over N days |
| `correlate_alarms` | Patterns across assets |
| `calculate_alarm_priority` | Priority score for an alarm |
| `get_operator_recommendations` | Recommended operator actions |

## Run (stdio)

```bash
cd mcp-servers/alarm-management
PYTHONPATH=../.. python3 server.py
```

Requires Alarm API on `ALARM_API_BASE_URL` (default `http://localhost:8000`) with `ALARM_API_TOKEN`.

## Copilot integration

`apps/backend/mcp_client.py` connects in-process, discovers tools, and invokes them during investigation. Results are combined with RAG via `search_procedures`.
