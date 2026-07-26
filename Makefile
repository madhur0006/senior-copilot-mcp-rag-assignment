.PHONY: help env simulator-up simulator-down test ingest retrieve investigate

help:
	@echo "Targets:"
	@echo "  make env             Copy .env.example to .env if missing"
	@echo "  make simulator-up    Start Alarm API simulator container"
	@echo "  make simulator-down  Stop Alarm API simulator container"
	@echo "  make ingest          Build RAG index (load→chunk→embed→Chroma)"
	@echo "  make retrieve        RAG grounded answer for a sample question"
	@echo "  make investigate     Full MCP+RAG copilot investigation"
	@echo "  make test            Run unit + integration tests"

env:
	@test -f .env || cp .env.example .env
	@echo ".env ready"

simulator-up:
	docker start alarm-api-simulator || \
	docker run -d \
	  --name alarm-api-simulator \
	  --platform linux/amd64 \
	  -e AUTH_ENABLED=true \
	  -p 8000:8000 \
	  alarm-api-simulator-alarm-api-simulator:latest

simulator-down:
	-docker stop alarm-api-simulator

ingest:
	PYTHONPATH=. python3 -m rag.ingestion.pipeline

retrieve:
	PYTHONPATH=. python3 -m rag.retrieval.grounded

investigate:
	PYTHONPATH=. python3 -m apps.backend

test-mcp-tools:
	PYTHONPATH=. python3 scripts/test_mcp_tools.py

test:
	PYTHONPATH=. python3 -m pytest tests/unit tests/integration

test-unit:
	PYTHONPATH=. python3 -m pytest tests/unit

test-integration:
	PYTHONPATH=. python3 -m pytest tests/integration

lint:
	@echo "Lint not wired yet (Step 9)."
