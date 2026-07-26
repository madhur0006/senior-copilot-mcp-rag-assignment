# Alarm Management MCP Server

MCP (Model Context Protocol) server that exposes Alarm Management API capabilities as tools.

## Tools Provided

| Tool | Purpose |
|------|---------|
| `search_assets` | Find assets by name or ID |
| `get_asset_metadata` | Get detailed asset information |
| `get_alarms` | List alarms with filters |
| `get_recent_critical_alarms` | Quick access to high/critical alarms |
| `correlate_alarms` | Find patterns across multiple assets |
| `calculate_alarm_priority` | Get priority score for an alarm |
| `get_operator_recommendations` | Get recommended actions |

## Running the Server

### Standalone (stdio transport)

```bash
cd mcp-servers/alarm-management
PYTHONPATH=../.. python server.py
```

### With MCP Inspector (for testing)

```bash
# Install MCP inspector if you haven't
npm install -g @modelcontextprotocol/inspector

# Run inspector pointing to this server
mcp-inspector python server.py
```

### Configuration

The server reads configuration from environment variables (same as the connector):

- `ALARM_API_BASE_URL` - API base URL (default: http://localhost:8000)
- `ALARM_API_TOKEN` - Bearer token (default: demo-token)

Create a `.env` file in the project root or set these variables.

## Testing Tools

Each tool can be tested via:
1. Unit tests (mock the connector)
2. Integration tests (live simulator)
3. MCP Inspector (interactive testing)

## Integration with Copilot

The copilot application (in `apps/backend`) will:
1. Connect to this MCP server as a client
2. Discover available tools
3. Call tools based on user queries
4. Combine tool results with RAG document retrieval
