.PHONY: help env simulator-up simulator-down test test-unit test-e2e coverage ingest retrieve investigate

help:
	@echo "Targets:"
	@echo "  make env             Copy .env.example to .env if missing"
	@echo "  make simulator-up    Start Alarm API simulator container"
	@echo "  make simulator-down  Stop Alarm API simulator container"
	@echo "  make ingest          Build RAG index (load→chunk→embed→Chroma)"
	@echo "  make retrieve        RAG grounded answer for a sample question"
	@echo "  make investigate     Full MCP+RAG copilot investigation"
	@echo "  make test            Unit + integration + e2e (live tests skip if unavailable)"
	@echo "  make test-unit       Unit tests only"
	@echo "  make test-e2e        End-to-end MCP+RAG tests"
	@echo "  make coverage        Unit + mocked e2e with HTML/XML coverage reports"

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
	PYTHONPATH=. python3 -m pytest tests/unit tests/integration tests/e2e

test-unit:
	PYTHONPATH=. python3 -m pytest tests/unit

test-integration:
	PYTHONPATH=. python3 -m pytest tests/integration

test-e2e:
	PYTHONPATH=. python3 -m pytest tests/e2e

coverage:
	PYTHONPATH=. python3 -m pytest \
	  tests/unit \
	  tests/e2e/test_investigation_mcp_rag.py::test_e2e_investigation_combines_mcp_and_rag_mocked \
	  --cov=apps \
	  --cov=connectors \
	  --cov=rag \
	  --cov-config=.coveragerc \
	  --cov-report=term-missing \
	  --cov-report=xml:coverage/coverage.xml \
	  --cov-report=html:coverage/html
	@echo "HTML report: coverage/html/index.html"
	@echo "XML report:  coverage/coverage.xml"

lint:
	@echo "Lint not wired yet."
