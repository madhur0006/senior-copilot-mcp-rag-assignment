# MCP Tool Catalog

Candidate MCP server: `mcp-servers/alarm-management`

> Fill each section during Step 4 implementation.

## Planned tools

| Tool | Purpose | Underlying API |
|---|---|---|
| `search_assets` | Resolve asset name to asset IDs | `GET /assets/search` |
| `get_asset_metadata` | Asset metadata / related context | `GET /assets/{asset_id}/metadata` |
| `get_alarms` | Active/historical alarms | `GET /alarms` |
| `correlate_alarms` | Alarm correlation | `POST /alarms/correlation` |
| `calculate_alarm_priority` | Priority scoring | `POST /alarms/priority-score` |
| `get_operator_recommendations` | Operator actions | `POST /recommendations/operator-actions` |

## Per-tool template (repeat for each tool)

### `<tool_name>`

- **Purpose:**
- **Input schema:**
- **Output schema:**
- **Authentication behavior:** Bearer token from config; not logged
- **Underlying source-system operation:**
- **Error behavior:** mapped API errors → MCP errors
- **Timeout behavior:**
- **Example invocation:**
- **Example response:**

## Independent start (to be filled)

```bash
# example later
python -m mcp_servers.alarm_management
```
