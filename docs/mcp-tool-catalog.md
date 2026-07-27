# MCP Tool Catalog

Candidate MCP server: `mcp-servers/alarm-management`

Transport: stdio (standalone) or in-process FastMCP Client (copilot).

Configuration (from `.env`):

| Variable | Default | Role |
|---|---|---|
| `ALARM_API_BASE_URL` | `http://localhost:8000` | Alarm API base |
| `ALARM_API_TOKEN` | `demo-token` | Bearer auth |
| `REQUEST_TIMEOUT_SECONDS` | `30` | HTTP timeout |
| `RETRY_COUNT` | `3` | Connector retries |

Authentication: connector sends `Authorization: Bearer <token>` plus client/trace headers. Token is never logged or returned in tool error messages.

Shared error behavior: API failures map to connector exceptions; the MCP client wraps unexpected failures as `{ "error": true, "tool": "...", "message": "...", "type": "..." }`.

Timeout / retry: handled in `connectors/alarm_api/client.py` (timeout + retry loop). Pagination: `page` / `page_size` on alarm list tools.

---

## Tool summary

| Tool | Purpose | Underlying API |
|---|---|---|
| `search_assets` | Resolve asset name/ID | `GET /assets/search` |
| `get_asset_metadata` | Asset details / related | `GET /assets/{asset_id}/metadata` |
| `get_alarms` | Filtered alarm list | `GET /alarms` |
| `get_recent_critical_alarms` | High/critical window | `GET /alarms` (severity + time range) |
| `correlate_alarms` | Cross-asset patterns | `POST /alarms/correlation` |
| `calculate_alarm_priority` | Priority score | `POST /alarms/priority-score` |
| `get_operator_recommendations` | Operator actions | `POST /recommendations/operator-actions` |

---

## `search_assets`

- **Purpose:** Find plant assets by name or ID.
- **Input schema:**
  - `query` (string, required) — search text
  - `site` (string, optional)
  - `unit` (string, optional)
  - `limit` (int, default 25)
- **Output schema:** API search payload (typically `results`, `total_results`).
- **Authentication:** Bearer from config.
- **Underlying operation:** `GET /assets/search`
- **Error behavior:** Auth/validation/not-found mapped via connector; client may return `{error: true, ...}`.
- **Timeout behavior:** Connector timeout + retries.
- **Example invocation:**

```json
{ "query": "Boiler Feed Pump 101", "limit": 5 }
```

- **Example response (shape):**

```json
{
  "total_results": 1,
  "results": [{ "asset_id": "AST00001", "name": "Boiler Feed Pump 101" }]
}
```

---

## `get_asset_metadata`

- **Purpose:** Detailed metadata, tags, and related assets.
- **Input schema:**
  - `asset_id` (string, required) — e.g. `AST00001`
- **Output schema:** Asset metadata object (tags, related assets, site/unit fields as provided by API).
- **Authentication:** Bearer from config.
- **Underlying operation:** `GET /assets/{asset_id}/metadata`
- **Error behavior:** `404` → not-found mapping; other HTTP errors mapped.
- **Timeout behavior:** Connector timeout + retries.
- **Example invocation:**

```json
{ "asset_id": "AST00001" }
```

- **Example response (shape):**

```json
{
  "asset_id": "AST00001",
  "related_assets": [],
  "tags": []
}
```

---

## `get_alarms`

- **Purpose:** List alarms with optional filters and pagination.
- **Input schema:**
  - `asset_id` (string, optional)
  - `severity` (string, optional) — `low` | `medium` | `high` | `critical` (sent to API as a list)
  - `status` (string, optional)
  - `page` (int, default 1)
  - `page_size` (int, default 50)
- **Output schema:** Paginated alarm list (API `data` / pagination fields).
- **Authentication:** Bearer from config.
- **Underlying operation:** `GET /alarms`
- **Error behavior:** Mapped connector errors / `{error: true}` wrapper.
- **Timeout behavior:** Connector timeout + retries.
- **Example invocation:**

```json
{ "asset_id": "AST00001", "severity": "high", "page_size": 10 }
```

- **Example response (shape):**

```json
{
  "data": [
    {
      "alarm_id": "ALM0035590",
      "asset_id": "AST00001",
      "severity": "high",
      "alarm_name": "Pump Discharge Pressure High"
    }
  ]
}
```

---

## `get_recent_critical_alarms`

- **Purpose:** Convenience window for high/critical alarms on one asset.
- **Input schema:**
  - `asset_id` (string, required)
  - `days` (int, default 7)
- **Output schema:** Same shape as `get_alarms` filtered to high/critical in the time window.
- **Authentication:** Bearer from config.
- **Underlying operation:** `GET /alarms` with `severity=["high","critical"]` and `start_time`/`end_time`.
- **Error behavior:** Same as `get_alarms`.
- **Timeout behavior:** Connector timeout + retries.
- **Example invocation:**

```json
{ "asset_id": "AST00001", "days": 90 }
```

- **Example response (shape):** alarm list under `data` for the last 90 days.

---

## `correlate_alarms`

- **Purpose:** Find co-occurrence patterns across assets.
- **Input schema:**
  - `asset_ids` (list[string], required)
  - `days` (int, default 7)
- **Output schema:** Correlation groups / patterns from API.
- **Authentication:** Bearer from config.
- **Underlying operation:** `POST /alarms/correlation`
- **Error behavior:** Mapped connector errors / `{error: true}` wrapper.
- **Timeout behavior:** Connector timeout + retries.
- **Example invocation:**

```json
{ "asset_ids": ["AST00001", "AST00002"], "days": 90 }
```

- **Example response (shape):**

```json
{ "correlation_groups": [] }
```

---

## `calculate_alarm_priority`

- **Purpose:** Priority score and contributing factors for one alarm.
- **Input schema:**
  - `alarm_id` (string, required)
- **Output schema:** Priority payload (`priority_score`, factors as provided by API).
- **Authentication:** Bearer from config.
- **Underlying operation:** `POST /alarms/priority-score`
- **Error behavior:** Mapped connector errors / `{error: true}` wrapper.
- **Timeout behavior:** Connector timeout + retries.
- **Example invocation:**

```json
{ "alarm_id": "ALM0035590" }
```

- **Example response (shape):**

```json
{ "alarm_id": "ALM0035590", "priority_score": 0.82 }
```

---

## `get_operator_recommendations`

- **Purpose:** API-recommended operator actions for an alarm.
- **Input schema:**
  - `alarm_id` (string, required)
- **Output schema:** Recommendations payload (`recommended_actions`, context flags).
- **Authentication:** Bearer from config.
- **Underlying operation:** `POST /recommendations/operator-actions`
- **Error behavior:** Mapped connector errors / `{error: true}` wrapper.
- **Timeout behavior:** Connector timeout + retries.
- **Example invocation:**

```json
{ "alarm_id": "ALM0035590" }
```

- **Example response (shape):**

```json
{
  "alarm_id": "ALM0035590",
  "recommended_actions": [
    { "action": "Verify transmitter reading against local gauge" }
  ]
}
```

---

## Independent start

```bash
# From repo root — Alarm API must be healthy on :8000
make simulator-up

cd mcp-servers/alarm-management
PYTHONPATH=../.. python3 server.py
```

Smoke helper:

```bash
PYTHONPATH=. python3 scripts/test_mcp_tools.py
```

Copilot discovery (same tool names):

```bash
PYTHONPATH=. python3 -c "from apps.backend.mcp_client import list_mcp_tools; print([t['name'] for t in list_mcp_tools()])"
```
