# Step 4: MCP Server - Line by Line Explanation

This document explains the MCP server code in simple, easy-to-understand terms.

## What is MCP?

**MCP = Model Context Protocol**

It's a standard way for AI assistants (like ChatGPT, Claude) to use tools. Think of it like a restaurant menu:
- The **menu** (MCP server) lists available dishes (tools)
- The **customer** (AI assistant) reads the menu and orders
- The **kitchen** (our code) makes the food and serves it

Our MCP server is the "menu + kitchen" that exposes alarm investigation tools.

---

## File: `mcp-servers/alarm-management/server.py`

### Part 1: Imports and Setup (Lines 1-23)

```python
"""
MCP Server for Alarm Management API.
Exposes alarm investigation tools via Model Context Protocol.
"""
```
**What it means**: This is a comment explaining what the file does.

```python
import sys
from pathlib import Path
from datetime import datetime, timedelta, timezone
```
**What it means**: 
- `sys` - lets us modify Python's import paths
- `Path` - helps us work with file paths
- `datetime` stuff - for working with dates and times

```python
# Add project root to path
ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
```
**What it means**: 
- Find the project root folder (2 levels up from this file)
- Add it to Python's search path
- So we can import `connectors.alarm_api` from anywhere

```python
from fastmcp import FastMCP
from connectors.alarm_api import AlarmApiClient, AlarmApiConfig
```
**What it means**:
- `FastMCP` - the library that makes creating MCP servers easy
- Import our Alarm API client from Step 3

```python
# Initialize MCP server
mcp = FastMCP("alarm-management")
```
**What it means**: Create an MCP server named "alarm-management". This is like opening a new restaurant.

```python
# Create shared alarm API client
alarm_client = None


def get_client():
    """Get or create the alarm API client."""
    global alarm_client
    if alarm_client is None:
        config = AlarmApiConfig()
        alarm_client = AlarmApiClient(config)
    return alarm_client
```
**What it means**: 
- Create ONE client and reuse it (saves memory)
- First time: create the client
- Next times: return the same client
- This is called the "Singleton pattern"

---

### Part 2: Tool 1 - Search Assets (Lines 25-42)

```python
@mcp.tool()
def search_assets(query: str, site: str = None, unit: str = None, limit: int = 25) -> dict:
```
**What it means**:
- `@mcp.tool()` - This decorator tells FastMCP "this function is a tool"
- Function name becomes the tool name
- Parameters become the tool's inputs
- `-> dict` means it returns a dictionary

```python
    """
    Search for assets by name or ID.
    
    Args:
        query: Search text (asset name or ID)
        site: Optional site filter
        unit: Optional unit filter
        limit: Maximum results to return
    
    Returns:
        Dictionary with search results and total count
    """
```
**What it means**: This docstring becomes the tool's description. AI assistants read this to understand what the tool does.

```python
    client = get_client()
    return client.search_assets(query, site=site, unit=unit, limit=limit)
```
**What it means**: 
- Get the alarm API client
- Call its `search_assets` method
- Pass along all the parameters
- Return the result

**Simple analogy**: 
- AI: "I need to find a pump"
- MCP Server: "Okay, I'll search for you"
- Client: Actually does the HTTP request to the API
- MCP Server: "Here are the results!"

---

### Part 3: Tool 2 - Get Asset Metadata (Lines 45-57)

```python
@mcp.tool()
def get_asset_metadata(asset_id: str) -> dict:
    """
    Get detailed metadata for a specific asset.
    
    Args:
        asset_id: The asset ID (e.g., AST00001)
    
    Returns:
        Dictionary with asset details, tags, and related assets
    """
    client = get_client()
    return client.get_asset_metadata(asset_id)
```
**What it means**: Same pattern as search_assets, but simpler - just takes an asset ID and returns its details.

---

### Part 4: Tool 3 - Get Alarms (Lines 60-91)

```python
@mcp.tool()
def get_alarms(
    asset_id: str = None,
    severity: str = None,
    status: str = None,
    page: int = 1,
    page_size: int = 50
) -> dict:
```
**What it means**: All parameters are optional (have default values). This makes the tool flexible.

```python
    client = get_client()
    
    # Convert single severity to list if provided
    severity_list = [severity] if severity else None
```
**What it means**: 
- The tool accepts a single severity string (easier for AI)
- But the client expects a list
- So we convert: "high" becomes ["high"]
- If no severity, keep it as None

```python
    return client.get_alarms(
        asset_id=asset_id,
        severity=severity_list,
        status=status,
        page=page,
        page_size=page_size
    )
```
**What it means**: Pass everything to the client and return results.

---

### Part 5: Tool 4 - Get Recent Critical Alarms (Lines 94-118)

```python
@mcp.tool()
def get_recent_critical_alarms(asset_id: str, days: int = 7) -> dict:
    """
    Get recent high/critical alarms for an asset.
    Convenience tool that filters by severity and time range.
    """
```
**What it means**: This is a "convenience tool" - it does something common (get recent critical alarms) without requiring the AI to calculate dates.

```python
    client = get_client()
    
    end = datetime.now(timezone.utc)
    start = end - timedelta(days=days)
```
**What it means**:
- Get current time (UTC)
- Calculate start time (X days ago)
- Example: if days=7, get alarms from the last week

```python
    return client.get_alarms(
        asset_id=asset_id,
        severity=["high", "critical"],
        start_time=start.isoformat().replace("+00:00", "Z"),
        end_time=end.isoformat().replace("+00:00", "Z"),
        page_size=50
    )
```
**What it means**:
- Automatically filter to high/critical severity
- Convert dates to ISO format with "Z" (the API's format)
- Return up to 50 results

**Why this tool exists**: Instead of the AI having to:
1. Calculate dates
2. Format dates
3. Set severity filters

It just calls one tool: `get_recent_critical_alarms("AST001", days=7)`

---

### Part 6: Tool 5 - Correlate Alarms (Lines 121-149)

```python
@mcp.tool()
def correlate_alarms(asset_ids: list, days: int = 7) -> dict:
    """
    Find correlations between alarms across multiple assets.
    """
```
**What it means**: Takes a list of asset IDs and finds patterns (which alarms happen together).

```python
    client = get_client()
    
    end = datetime.now(timezone.utc)
    start = end - timedelta(days=days)
    
    payload = {
        "asset_ids": asset_ids,
        "time_range": {
            "start_time": start.isoformat().replace("+00:00", "Z"),
            "end_time": end.isoformat().replace("+00:00", "Z"),
        },
        "correlation_method": "cooccurrence",
        "lag_window_minutes": 15,
        "severity_threshold": "medium",
        "min_support": 1,
    }
    
    return client.correlate_alarms(payload)
```
**What it means**:
- Build a complex payload (all the parameters the API needs)
- Use sensible defaults:
  - `cooccurrence` - find alarms that happen at the same time
  - `lag_window_minutes: 15` - within 15 minutes counts as "same time"
  - `severity_threshold: medium` - ignore low-severity alarms
  - `min_support: 1` - show all correlations (even if they happened once)

**Why this tool exists**: The API's correlation endpoint is complex. This tool hides that complexity.

---

### Part 7: Tool 6 & 7 - Priority and Recommendations (Lines 152-177)

```python
@mcp.tool()
def calculate_alarm_priority(alarm_id: str) -> dict:
    """Calculate priority score for an alarm."""
    client = get_client()
    return client.get_priority_score(alarm_id)


@mcp.tool()
def get_operator_recommendations(alarm_id: str) -> dict:
    """Get recommended operator actions for an alarm."""
    client = get_client()
    return client.get_operator_recommendations(alarm_id)
```
**What it means**: Two simple tools that just wrap the client methods. No extra logic needed.

---

### Part 8: Running the Server (Lines 180-182)

```python
if __name__ == "__main__":
    # Run with stdio transport (for local use with MCP clients)
    mcp.run()
```
**What it means**:
- `if __name__ == "__main__"` - only run this if the file is executed directly
- `mcp.run()` - start the MCP server
- Uses "stdio" transport by default (standard input/output - the server talks via text)

---

## How It All Works Together

```
┌─────────────────┐
│   AI Assistant  │  "Show critical alarms for pump 101"
│   (like Claude) │
└────────┬────────┘
         │ 1. Discovers tools (reads descriptions)
         │ 2. Decides to call search_assets + get_recent_critical_alarms
         ▼
┌─────────────────┐
│   MCP Server    │  Our server.py
│  (this file)    │
└────────┬────────┘
         │ 3. Executes the tools
         │ 4. Calls AlarmApiClient
         ▼
┌─────────────────┐
│  AlarmApiClient │  From Step 3
│ (connector)     │
└────────┬────────┘
         │ 5. Makes HTTP requests
         ▼
┌─────────────────┐
│   Alarm API     │  Docker simulator
│   Simulator     │
└─────────────────┘
         │ 6. Returns data
         │
         ▼
      (Results flow back up)
```

---

## Key Concepts

### 1. Why use `@mcp.tool()`?
- FastMCP automatically:
  - Registers the function as a tool
  - Creates a JSON schema from type hints
  - Reads the docstring as the description
  - Handles calling the function when requested

### 2. Why `global alarm_client`?
- Creating a new client for every request wastes memory
- One client can handle all requests
- It reuses the HTTP connection pool

### 3. Why wrap the AlarmApiClient?
- The client knows HOW to call the API (HTTP details)
- The MCP tools know WHAT operations make sense for AI assistants
- Separation of concerns

### 4. Why convenience tools like `get_recent_critical_alarms`?
- AI assistants work better with task-oriented tools
- "Get recent critical alarms" is clearer than "Get alarms with time range and severity filter"
- Less chance of mistakes

---

## Testing the MCP Server

### Manual test script: `scripts/test_mcp_tools.py`
Directly imports and calls each tool to verify they work.

### How to run:
```bash
# Activate venv
source .venv/bin/activate

# Make sure simulator is running
docker ps | grep alarm-api

# Run test
PYTHONPATH=. python3 scripts/test_mcp_tools.py
```

### What it tests:
1. Search for an asset
2. Get its metadata
3. Get recent critical alarms
4. Calculate priority for an alarm
5. Get recommendations
6. Correlate alarms
7. Get filtered alarms

---

## Summary

The MCP server is a **thin wrapper** around the AlarmApiClient that:
- Exposes 7 tools for alarm investigation
- Makes complex API operations simple for AI assistants
- Handles date calculations and payload building
- Provides clear descriptions for each tool

Think of it as a waiter at a restaurant:
- The menu (tool descriptions) is clear
- You order (AI calls a tool)
- The waiter (MCP server) tells the kitchen (client)
- The kitchen (client) prepares the food (API call)
- You get your meal (results)
