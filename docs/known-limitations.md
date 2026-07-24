# Known Limitations

Living list — update during implementation.

## Current

1. Copilot backend, MCP server, GUI, and tests are not implemented yet (skeleton only).
2. `docker-compose.yml` currently documents the alarm-api service; MCP/backend/frontend services are commented placeholders.
3. Architecture diagram image (`architecture-diagram.png`) is not added yet.
4. Supplied simulator image is amd64-only; arm64 hosts need emulation/Rosetta.
5. Large simulator tar is excluded from git by `.gitignore` due to size.

## Future improvements

- Full Compose one-command startup for all services
- Richer observability dashboards
- Stronger hybrid retrieval / reranking
- More failure-path demos in GUI
