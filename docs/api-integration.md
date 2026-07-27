# API Integration

## Source system

Alarm Management API Simulator in `alarm-management-api-simulator/`.

| Item | Value |
|---|---|
| Base URL (local) | `http://localhost:8000` |
| Auth | `Authorization: Bearer demo-token` when `AUTH_ENABLED=true` |
| Swagger | http://localhost:8000/docs |
| OpenAPI | http://localhost:8000/openapi.json |

## Boundary rule

The **copilot orchestration layer must not call the Alarm API directly**.  
Only the MCP server (via `connectors/alarm_api`) talks to the Alarm API.  
The agent invokes MCP tools through `apps/backend/mcp_client.py`.

## Operations used

| Capability | Method / path | MCP tool |
|---|---|---|
| Health | `GET /health` | (connector smoke) |
| Asset search | `GET /assets/search` | `search_assets` |
| Asset metadata | `GET /assets/{asset_id}/metadata` | `get_asset_metadata` |
| Alarms | `GET /alarms` | `get_alarms`, `get_recent_critical_alarms` |
| Correlation | `POST /alarms/correlation` | `correlate_alarms` |
| Priority score | `POST /alarms/priority-score` | `calculate_alarm_priority` |
| Operator recommendations | `POST /recommendations/operator-actions` | `get_operator_recommendations` |

## Connector

Code: `connectors/alarm_api/`

- `config.py` — `.env` (`ALARM_API_BASE_URL`, `ALARM_API_TOKEN`, timeout, retries)
- `client.py` — `AlarmApiClient` with auth, retries, trace headers
- `errors.py` — `AlarmApiAuthError`, timeout, validation, not-found

Live check:

```bash
PYTHONPATH=. python3 -c "from connectors.alarm_api import AlarmApiClient; print(AlarmApiClient().health())"
```

## Cross-cutting concerns

- Timeout and retry in the connector
- Pagination for alarm lists (`page`, `page_size`)
- Trace headers (`trace_id`, client id, metadata tag) where supported
- HTTP errors mapped to clear connector/MCP errors
- Bearer token never logged or returned in GUI traces

## Local Apple Silicon

Supplied image is `linux/amd64`. On arm64 Macs:

```bash
docker run -d --name alarm-api-simulator --platform linux/amd64 \
  -e AUTH_ENABLED=true -p 8000:8000 \
  alarm-api-simulator-alarm-api-simulator:latest
```

Or: `make simulator-up`
