@echo off
setlocal EnableExtensions EnableDelayedExpansion

REM Usage:
REM   start.bat [tar_path] [image_name] [container_name] [host_port] [container_port] [auth_enabled]
REM Example:
REM   start.bat alarm-api-simulator_latest.tar alarm-api-simulator-alarm-api-simulator:latest alarm-api-simulator 8000 8000 true

set "TAR_PATH=%~1"
if "%TAR_PATH%"=="" set "TAR_PATH=alarm-api-simulator_latest.tar"

set "IMAGE_NAME=%~2"
if "%IMAGE_NAME%"=="" set "IMAGE_NAME=alarm-api-simulator-alarm-api-simulator:latest"

set "CONTAINER_NAME=%~3"
if "%CONTAINER_NAME%"=="" set "CONTAINER_NAME=alarm-api-simulator"

set "HOST_PORT=%~4"
if "%HOST_PORT%"=="" set "HOST_PORT=8000"

set "CONTAINER_PORT=%~5"
if "%CONTAINER_PORT%"=="" set "CONTAINER_PORT=8000"

set "AUTH_ENABLED=%~6"
if "%AUTH_ENABLED%"=="" set "AUTH_ENABLED=true"

echo ============================================================
echo Alarm API Simulator - start.bat
echo ============================================================
echo Inputs:
echo   TAR_PATH      = %TAR_PATH%
echo   IMAGE_NAME    = %IMAGE_NAME%
echo   CONTAINER_NAME= %CONTAINER_NAME%
echo   HOST_PORT     = %HOST_PORT%
echo   CONTAINER_PORT= %CONTAINER_PORT%
echo   AUTH_ENABLED  = %AUTH_ENABLED%  ^(app default and script default are true^)
echo ============================================================

echo [1/7] Checking Docker CLI...
where docker >nul 2>&1
if errorlevel 1 (
  echo ERROR: Docker CLI is not available in PATH.
  exit /b 1
)
echo Docker CLI found.
for /f "usebackq delims=" %%V in (`docker --version 2^>^&1`) do echo %%V

echo [2/7] Verifying Docker daemon availability...
docker info >nul 2>&1
if errorlevel 1 (
  echo ERROR: Docker daemon is not running or not reachable.
  echo Start Docker Desktop/service and retry.
  exit /b 1
)
echo Docker daemon is reachable.

echo [3/7] Validating tar file...
if not exist "%TAR_PATH%" (
  echo ERROR: Tar file not found: %TAR_PATH%
  exit /b 1
)
for %%F in ("%TAR_PATH%") do echo Tar size: %%~zF bytes

echo [4/7] Loading Docker image from tar: %TAR_PATH%
set "LOADED_LINE="
set "LOAD_LOG=%TEMP%\alarm_api_simulator_docker_load.log"
docker load -i "%TAR_PATH%" >"%LOAD_LOG%" 2>&1
set "LOAD_RC=%ERRORLEVEL%"
for /f "usebackq delims=" %%L in ("%LOAD_LOG%") do (
  echo %%L
  echo %%L | findstr /c:"Loaded image:" >nul
  if not errorlevel 1 set "LOADED_LINE=%%L"
)
if not "%LOAD_RC%"=="0" (
  echo ERROR: docker load failed.
  if exist "%LOAD_LOG%" type "%LOAD_LOG%"
  exit /b 1
)

if defined LOADED_LINE (
  set "DETECTED_IMAGE=!LOADED_LINE:Loaded image:=!"
  for /f "tokens=* delims= " %%I in ("!DETECTED_IMAGE!") do set "DETECTED_IMAGE=%%I"
  if not "!DETECTED_IMAGE!"=="" set "IMAGE_NAME=!DETECTED_IMAGE!"
)
echo Effective image to run: %IMAGE_NAME%

echo [5/7] Confirming image exists locally...
docker image inspect "%IMAGE_NAME%" >nul 2>&1
if errorlevel 1 (
  echo ERROR: Image '%IMAGE_NAME%' not found after docker load.
  exit /b 1
)
echo Image is available locally.
for /f "usebackq tokens=* delims=" %%S in (`docker images "%IMAGE_NAME%" --format "{{.Repository}}:{{.Tag}}  id={{.ID}}  size={{.Size}}"`) do echo %%S

echo [6/7] Replacing existing container if present: %CONTAINER_NAME%
set "EXISTING_CONTAINER="
for /f "delims=" %%C in ('docker ps -a --filter "name=^/%CONTAINER_NAME%$" --format "{{.Names}}"') do set "EXISTING_CONTAINER=%%C"
if defined EXISTING_CONTAINER (
  echo Existing container found. Removing...
  docker rm -f "%CONTAINER_NAME%"
) else (
  echo No existing container found with this name.
)

echo [7/7] Starting container...
set "RUN_LOG=%TEMP%\alarm_api_simulator_docker_run.log"
docker run -d --name "%CONTAINER_NAME%" -e AUTH_ENABLED=%AUTH_ENABLED% -p %HOST_PORT%:%CONTAINER_PORT% "%IMAGE_NAME%" >"%RUN_LOG%" 2>&1
set "RUN_RC=%ERRORLEVEL%"
set "RUN_OUTPUT="
for /f "usebackq delims=" %%I in ("%RUN_LOG%") do (
  echo %%I
  set "RUN_OUTPUT=%%I"
)
if not "%RUN_RC%"=="0" (
  echo ERROR: Failed to start container from image %IMAGE_NAME%
  if exist "%RUN_LOG%" type "%RUN_LOG%"
  exit /b 1
)
echo Container ID: %RUN_OUTPUT%

echo Current container status:
docker ps --filter "name=^/%CONTAINER_NAME%$" --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"

echo.
echo Container started successfully.
echo Health URL : http://localhost:%HOST_PORT%/health
echo Swagger URL: http://localhost:%HOST_PORT%/docs
echo.
timeout /t 2 >nul
powershell -NoProfile -Command "$ProgressPreference='SilentlyContinue'; try { $r = Invoke-RestMethod -Uri 'http://localhost:%HOST_PORT%/health' -TimeoutSec 15; Write-Host ('Health response: ' + ($r | ConvertTo-Json -Compress)); } catch { Write-Host 'Health check not ready yet. You can retry in a few seconds.'; }"
echo.
echo Recent container logs:
docker logs --tail 20 "%CONTAINER_NAME%"

endlocal
exit /b 0
