@echo off
setlocal EnableExtensions

REM Usage:
REM   stop.bat [container_name]
REM Example:
REM   stop.bat alarm-api-simulator

set "CONTAINER_NAME=%~1"
if "%CONTAINER_NAME%"=="" set "CONTAINER_NAME=alarm-api-simulator"

echo [1/3] Checking Docker CLI...
where docker >nul 2>&1
if errorlevel 1 (
  echo ERROR: Docker CLI is not available in PATH.
  exit /b 1
)

echo [2/3] Looking for container: %CONTAINER_NAME%
set "EXISTS="
for /f "delims=" %%C in ('docker ps -a --filter "name=^/%CONTAINER_NAME%$" --format "{{.Names}}"') do set "EXISTS=%%C"

if not defined EXISTS (
  echo Container '%CONTAINER_NAME%' not found. Nothing to stop.
  exit /b 0
)

echo [3/3] Stopping and removing container: %CONTAINER_NAME%
docker rm -f "%CONTAINER_NAME%" >nul
if errorlevel 1 (
  echo ERROR: Failed to remove container '%CONTAINER_NAME%'.
  exit /b 1
)

echo Container '%CONTAINER_NAME%' stopped and removed successfully.
endlocal
exit /b 0
