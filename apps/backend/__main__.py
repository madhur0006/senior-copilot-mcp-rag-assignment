"""
Run the copilot investigation from the command line.

  docker start alarm-api-simulator
  PYTHONPATH=. python3 -m apps.backend
"""
from apps.backend.mcp_client import list_mcp_tools
from apps.backend.service import run_investigation
from rag.ingestion.config import RagConfig

DEFAULT_QUERY = (
    "Investigate recurring high-severity alarms for Boiler Feed Pump 101 "
    "over the last 90 days, identify likely contributing factors, retrieve "
    "the relevant operating procedure, and provide recommended actions with "
    "source evidence."
)


def main():
    config = RagConfig()
    print(f"Provider: {config.provider}")
    print(f"Chat:     {config.chat_model}")
    print(f"Index:    {config.index_dir}")

    print("\n=== MCP tools ===")
    for t in list_mcp_tools():
        print(f"  - {t['name']}")

    query = DEFAULT_QUERY
    print(f"\n=== Investigation ===\n{query}\n")

    result = run_investigation(query, config=config)

    print("--- Tool trace ---")
    for i, item in enumerate(result.tool_trace, 1):
        status = "OK" if item.ok else "ERR"
        print(f"{i}. [{status}] {item.tool} args={item.arguments}")
        print(f"   → {item.result_preview[:180]}")

    print("\n--- Citations ---")
    for c in result.citations:
        print(f"  - {c.get('doc_id')} | {c.get('section')} | {c.get('source_path')}")

    print("\n--- Answer ---\n")
    print(result.answer)


if __name__ == "__main__":
    main()
