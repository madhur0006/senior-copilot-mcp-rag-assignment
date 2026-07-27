# Known Limitations

## Current

1. `docker compose up` only starts the Alarm API; MCP, backend, and Streamlit GUI run locally via `PYTHONPATH` / Makefile (not full Compose packaging yet).
2. Supplied simulator image is amd64-only; Apple Silicon needs `--platform linux/amd64` (Rosetta).
3. Large simulator tar is gitignored (`alarm-management-api-simulator/*.tar`); load it locally before first run.
4. No dedicated automated GUI e2e test yet; backend e2e covers MCP+RAG via `tests/e2e/` (mocked in CI, live when services are up).
5. Observability is limited to MCP tool-trace in the GUI (no full request/trace ID logging pipeline).
6. Context overflow can still occur on very chatty tool loops; tool outputs are compacted to reduce risk.
7. Demo video and screenshots are not yet linked in the README.

## Future improvements

- Full Compose one-command startup (API + MCP + backend + GUI)
- Richer observability (request/trace IDs, latencies)
- Stronger hybrid retrieval / reranking
- Automated GUI e2e scenario and broader MCP contract tests
- Demo video + screenshots linked from README
- Coverage report in CI artifacts
