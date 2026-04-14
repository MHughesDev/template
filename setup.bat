@echo off
REM setup.bat — Windows bootstrap (requires Python 3.12+ on PATH)
setlocal
cd /d "%~dp0"
where python >nul 2>nul || (echo Python not found & exit /b 1)
if not exist .venv python -m venv .venv
call .venv\Scripts\activate.bat
python -m pip install --upgrade pip
pip install -e ".[dev]"
if not exist .env copy .env.example .env
set PYTHONPATH=%CD%
make migrate
echo Setup complete. Run run.bat or make dev.
endlocal
