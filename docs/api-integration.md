# API Integration

## Source system

Alarm Management API Simulator provided in `alarm-management-api-simulator/`.

- Base URL (local): `http://localhost:8000`
- Auth: `Authorization: Bearer demo-token` when `AUTH_ENABLED=true`
- Docs: `http://localhost:8000/docs`
- OpenAPI: `http://localhost:8000/openapi.json`

## Important rule (ABB)

The **copilot orchestration layer must not call the Alarm API directly**.  
Only the MCP server (via connectors) talks to the Alarm API.

## Key operations used by this use case

| Capability | Method / path |
|---|---|
| Health | `GET /health` |
| Asset search | `GET /assets/search` |
| Asset metadata | `GET /assets/{asset_id}/metadata` |
| Alarms | `GET /alarms` |
| Alarm by ID | `GET /alarms/{alarm_id}` |
| Summary | `POST /alarms/summary` |
| Trends | `POST /alarms/trends` |
| Correlation | `POST /alarms/correlation` |
| Priority score | `POST /alarms/priority-score` |
| Operator recommendations | `POST /recommendations/operator-actions` |

## Connector implementation (Step 3)

Code lives in `connectors/alarm_api/`:

- `config.py` — reads `.env` (`ALARM_API_BASE_URL`, `ALARM_API_TOKEN`, timeouts, retries)
- `client.py` — `AlarmApiClient` with auth, retries, trace headers, convenience methods
- `errors.py` — mapped errors (`AlarmApiAuthError`, timeout, validation, not found)

Smoke check:

```bash
python scripts/smoke_alarm_api_client.py
```

Unit + live tests:

```bash
python -m pytest tests/unit tests/integration
```

## Cross-cutting concerns

- Timeout and retry in connector
- Pagination for alarm lists
- Trace headers (`trace_id` / `trace-id`, `x-client-id`, `x-metadata-tag`) where supported
- Map HTTP errors into clear connector/MCP errors
- Never log the raw bearer token

## Local Apple Silicon note

Supplied image is `linux/amd64`. On arm64 Macs with Rancher Desktop, run with:

```bash
docker run -d --name alarm-api-simulator --platform linux/amd64 \
  -e AUTH_ENABLED=true -p 8000:8000 \
  alarm-api-simulator-alarm-api-simulator:latest
```

Rosetta/VzRosetta should be enabled if QEMU segfaults occur.
