# Known limitations

- Compose currently starts only the Alarm API. Run MCP / Streamlit separately (`Makefile` / `PYTHONPATH`).
- Simulator image is amd64 (`make simulator-up` already passes `--platform linux/amd64`).
- Simulator `.tar` is gitignored (large). Load it once locally before first run.
- No Selenium-style GUI e2e; backend e2e covers MCP + RAG.
- Tool trace in the UI is the main observability. No full metrics stack.
- Very large tool loops can still hit LLM context limits (outputs are compacted to reduce that).
