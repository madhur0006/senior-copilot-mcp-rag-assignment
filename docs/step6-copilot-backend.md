# Step 6 — Copilot backend (MCP + LangGraph + RAG)

## Goal

Combine **MCP alarm tools** and **RAG procedures** in one investigation workflow with a **tool trace** and **citations**.

## Explicit LangGraph (in `agent.py`)

```text
START → agent ──(tools_condition)──► tools → agent → … → END
              └────────────────────► END (final answer, no tool_calls)
```

- `llm.bind_tools(COPILOT_TOOLS)` — model can request MCP/RAG tools
- `agent` node — LLM decides next tool call or final answer
- `tools` node — `ToolNode(COPILOT_TOOLS)` executes them
- loop until the model returns a normal message (no tool calls)

## Run

```bash
docker start alarm-api-simulator
PYTHONPATH=. python3 -m rag.ingestion.pipeline   # once, if index missing
PYTHONPATH=. python3 -m apps.backend
```

Or:

```python
from apps.backend import run_investigation
result = run_investigation("Investigate Boiler Feed Pump 101 high-severity alarms...")
print(result.answer)
print(result.tool_trace)
```
