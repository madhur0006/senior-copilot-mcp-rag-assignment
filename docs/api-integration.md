# API integration

## Source

Alarm Management API simulator under `alarm-management-api-simulator/`.

| | |
|---|---|
| Base URL | `http://localhost:8000` |
| Auth | `Authorization: Bearer demo-token` when `AUTH_ENABLED=true` |
| Swagger | http://localhost:8000/docs |
| OpenAPI | http://localhost:8000/openapi.json |

## Important boundary

The agent / orchestration code does not call this API directly.  
Calls go: agent → MCP client → MCP server → `connectors/alarm_api` → HTTP.

## Endpoints used

| Capability | API | MCP tool |
|---|---|---|
| Health | `GET /health` | (smoke via connector) |
| Asset search | `GET /assets/search` | `search_assets` |
| Asset metadata | `GET /assets/{id}/metadata` | `get_asset_metadata` |
| Alarms | `GET /alarms` | `get_alarms`, `get_recent_critical_alarms` |
| Correlation | `POST /alarms/correlation` | `correlate_alarms` |
| Priority | `POST /alarms/priority-score` | `calculate_alarm_priority` |
| Recommendations | `POST /recommendations/operator-actions` | `get_operator_recommendations` |

## Connector

`connectors/alarm_api/`:

- `config.py` – env for base URL, token, timeout, retries
- `client.py` – requests + retries + trace headers
- `errors.py` – auth / timeout / validation / not-found

Quick check:

```bash
PYTHONPATH=. python3 -c "from connectors.alarm_api import AlarmApiClient; print(AlarmApiClient().health())"
```

## Other behaviour

- Retries and timeouts live in the connector
- Alarm list calls support pagination
- Trace / client headers are sent when the API accepts them
- Token is not written into GUI tool previews

## Apple Silicon

Image is `linux/amd64`. Prefer:

```bash
make simulator-up
```

or run with `--platform linux/amd64` yourself.
