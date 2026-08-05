# Alarm API Simulator Artifacts Usage

This folder contains everything needed to run the simulator on another Windows machine using Docker image tar import.

## Included Files

- `alarm-api-simulator_latest.tar` - Docker image archive.
- `alarm-api-simulator_latest.sha256.txt` - Size and SHA256 checksum.
- `start.bat` - Loads tar, starts container, and prints health/logs.
- `stop.bat` - Stops and removes a container by name.
- `postman/Alarm-API-Simulator.postman_collection.json` - Importable Postman collection.
- `postman/scenarios/Alarm-API-Scenarios.postman_collection.json` - Scenario-focused API collection.
- `postman/chaining/Alarm-API-Chaining.postman_collection.json` - 10 multi-step chaining workflows.

## Prerequisites

- Docker Desktop installed and running.
- Windows PowerShell or Command Prompt.

## 1) Verify Tar Integrity (Recommended)

From this folder:

```powershell
Get-FileHash .\alarm-api-simulator_latest.tar -Algorithm SHA256
Get-Content .\alarm-api-simulator_latest.sha256.txt
```

Confirm the hash matches the value in `alarm-api-simulator_latest.sha256.txt`.

## 2) Start the Simulator from Tar

Default start (auth enabled by default):

```cmd
start.bat
```

Full argument form:

```cmd
start.bat [tar_path] [image_name] [container_name] [host_port] [container_port] [auth_enabled]
```

Example with explicit values:

```cmd
start.bat alarm-api-simulator_latest.tar alarm-api-simulator-alarm-api-simulator:latest alarm-api-simulator 8000 8000 true
```

## 3) Disable Auth (Optional)

To run in no-auth simulator mode:

```cmd
start.bat alarm-api-simulator_latest.tar alarm-api-simulator-alarm-api-simulator:latest alarm-api-simulator 8000 8000 false
```

Behavior:
- `auth_enabled=true`: APIs require non-empty `Authorization` header.
- `auth_enabled=false`: APIs work without `Authorization` header.

## 4) Stop the Simulator

Default container name:

```cmd
stop.bat
```

Specific container name:

```cmd
stop.bat alarm-api-simulator
```

## 5) URLs After Start

If started with host port `8000`:

- Health: `http://localhost:8000/health`
- Swagger: `http://localhost:8000/docs`
- OpenAPI JSON: `http://localhost:8000/openapi.json`

## 6) Postman Usage

1. Open Postman.
2. Import:
   - `postman/Alarm-API-Simulator.postman_collection.json` (complete E2E baseline)
   - `postman/scenarios/Alarm-API-Scenarios.postman_collection.json` (scenario tests)
   - `postman/chaining/Alarm-API-Chaining.postman_collection.json` (chaining flows)
3. Set collection variable `baseUrl` if you changed port.
4. Run requests in order for chained variables (`asset_id`, `alarm_id`, `calculation_id`).

Recommended headers when auth is enabled:

- `Authorization: Bearer demo-token`
- `trace_id: trace-001`
- `x-client-id: postman-client`
- `x-metadata-tag: smoke`

## 7) Quick Smoke Commands

Auth enabled check (should return 401):

```powershell
Invoke-WebRequest "http://localhost:8000/alarms" -Method GET
```

Auth enabled with header (should return 200):

```powershell
Invoke-WebRequest "http://localhost:8000/alarms" -Headers @{ Authorization = "Bearer demo-token" }
```

## 8) Troubleshooting

- If `docker` is not found: add Docker CLI to PATH and restart shell.
- If daemon is unreachable: start Docker Desktop.
- If port already in use: choose another host port in `start.bat` arguments.
- If container exists with same name: `start.bat` will replace it automatically.
