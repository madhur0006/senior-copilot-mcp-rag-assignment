# Known limitations

Deliberate scope choices for this assignment demo:

- Compose starts the Alarm API simulator. MCP and Streamlit are started with Make / `PYTHONPATH` (see README Quick start).
- Simulator image is amd64; `make simulator-up` passes `--platform linux/amd64`.
- Simulator `.tar` is gitignored (large). Load it once locally before the first run.
- Backend e2e covers MCP + RAG. There is no Selenium-style browser GUI e2e.
- Observability is the Streamlit tool trace (no separate metrics stack).
- Tool outputs are compacted before they go back to the model to keep LLM context under control.
