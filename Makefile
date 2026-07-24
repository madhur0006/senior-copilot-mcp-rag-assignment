.PHONY: help env simulator-up simulator-down test lint format

help:
	@echo "Targets:"
	@echo "  make env             Copy .env.example to .env if missing"
	@echo "  make simulator-up    Start Alarm API simulator container"
	@echo "  make simulator-down  Stop Alarm API simulator container"
	@echo "  make test            Run tests (filled in later steps)"
	@echo "  make lint            Run lint (filled in later steps)"

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

smoke-alarm-api:
	PYTHONPATH=. python scripts/smoke_alarm_api_client.py

test:
	PYTHONPATH=. python -m pytest tests/unit tests/integration

test-unit:
	PYTHONPATH=. python -m pytest tests/unit

test-integration:
	PYTHONPATH=. python -m pytest tests/integration

lint:
	@echo "Lint not wired yet (Step 9)."
