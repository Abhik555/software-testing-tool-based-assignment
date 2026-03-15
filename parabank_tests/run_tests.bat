@echo off
echo =======================================================
echo ParaBank Test Suite Execution Script
echo =======================================================

:: Navigate to the script's directory exactly where tests reside
cd /d "%~dp0"

echo [1/3] Checking for uv installation...
where uv >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo Error: 'uv' is not installed or not in PATH.
    echo Please install uv before running this script.
    pause
    exit /b 1
)

echo [2/3] Setting up Python virtual environment via uv...
if not exist ".venv" (
    echo Creating virtual environment...
    call uv venv
) else (
    echo Virtual environment already exists.
)

echo Installing dependencies...
call uv pip install -r requirements.txt

echo [3/3] Executing test suite...
:: Running pytest via uv which automatically uses the local .venv
call uv run pytest

echo.
echo =======================================================
echo Test execution complete! 
echo Check 'report.html' for detailed results and 'screenshots/' for failure captures.
echo =======================================================
pause
