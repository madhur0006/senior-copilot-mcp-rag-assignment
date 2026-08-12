# MCP tool catalog

Server: `mcp-servers/alarm-management`

Can run as stdio (`python3 server.py`) or be used in-process by the copilot MCP client.

## Config

| Env | Default | Use |
|---|---|---|
| `ALARM_API_BASE_URL` | `http://localhost:8000` | API base |
| `ALARM_API_TOKEN` | `demo-token` | Bearer token |
| `REQUEST_TIMEOUT_SECONDS` | `30` | HTTP timeout |
| `RETRY_COUNT` | `3` | connector retries |

Auth: connector adds `Authorization: Bearer …` plus client/trace headers. Token is not logged and not returned in tool error payloads.

Errors: HTTP failures become connector exceptions. Unexpected MCP client failures come back as `{ "error": true, "tool": "...", "message": "...", "type": "..." }`.

Timeouts / retries: `connectors/alarm_api/client.py`.  
Pagination: `page` / `page_size` on list calls.

## Summary

| Tool | Purpose | API |
|---|---|---|
| `search_assets` | Find assets | `GET /assets/search` |
| `get_asset_metadata` | Asset details | `GET /assets/{asset_id}/metadata` |
| `get_alarms` | Filtered alarms | `GET /alarms` |
| `get_recent_critical_alarms` | High/critical window | `GET /alarms` |
| `correlate_alarms` | Cross-asset patterns | `POST /alarms/correlation` |
| `calculate_alarm_priority` | Priority score | `POST /alarms/priority-score` |
| `get_operator_recommendations` | Recommended actions | `POST /recommendations/operator-actions` |

---

## `search_assets`

Find assets by name or id.

**Input**

- `query` (string, required)
- `site` (string, optional)
- `unit` (string, optional)
- `limit` (int, default 25)

**Output:** API search payload (`results`, `total_results`, …)

**Example**

```json
{ "query": "Boiler Feed Pump 101", "limit": 5 }
```

```json
{
  "total_results": 1,
  "results": [{ "asset_id": "AST00001", "name": "Boiler Feed Pump 101" }]
}
```

---

## `get_asset_metadata`

Details / tags / related assets for one id.

**Input:** `asset_id` (string, required)

**Example**

```json
{ "asset_id": "AST00001" }
```

```json
{
  "asset_id": "AST00001",
  "related_assets": [],
  "tags": []
}
```

404 from the API is mapped to a not-found style error.

---

## `get_alarms`

List alarms with filters.

**Input**

- `asset_id` (optional)
- `severity` (optional: low/medium/high/critical – sent to the API as a list)
- `status` (optional)
- `page` (default 1)
- `page_size` (default 50)

**Example**

```json
{ "asset_id": "AST00001", "severity": "high", "page_size": 10 }
```

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

Helper around `get_alarms` for high/critical in the last N days.

**Input**

- `asset_id` (required)
- `days` (default 7)

Builds `start_time` / `end_time` and `severity=["high","critical"]`.

**Example**

```json
{ "asset_id": "AST00001", "days": 90 }
```

Response shape matches the alarm list (`data`, …).

---

## `correlate_alarms`

Co-occurrence style correlation across assets.

**Input**

- `asset_ids` (list of strings)
- `days` (default 7)

**Example**

```json
{ "asset_ids": ["AST00001", "AST00002"], "days": 90 }
```

```json
{ "correlation_groups": [] }
```

---

## `calculate_alarm_priority`

Priority score for one alarm.

**Input:** `alarm_id`

**Example**

```json
{ "alarm_id": "ALM0035590" }
```

```json
{ "alarm_id": "ALM0035590", "priority_score": 0.82 }
```

Exact factor fields depend on what the simulator returns.

---

## `get_operator_recommendations`

API recommended actions for one alarm.

**Input:** `alarm_id`

**Example**

```json
{ "alarm_id": "ALM0035590" }
```

```json
{
  "alarm_id": "ALM0035590",
  "recommended_actions": [
    { "action": "Verify transmitter reading against local gauge" }
  ]
}
```

---

## How to run / smoke test

```bash
make simulator-up
cd mcp-servers/alarm-management
PYTHONPATH=../.. python3 server.py
```

```bash
PYTHONPATH=. python3 -c "from apps.backend.mcp_client import list_mcp_tools; print([t['name'] for t in list_mcp_tools()])"
```
