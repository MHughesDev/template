@echo off
REM setup.bat — Windows bootstrap (Python 3.12+, Docker, Make, Git on PATH)
setlocal enabledelayedexpansion
cd /d "%~dp0"

where python >nul 2>nul || (echo ERROR: Python not found on PATH & exit /b 1)
where docker >nul 2>nul || (echo ERROR: Docker not found on PATH & exit /b 1)
where make >nul 2>nul || (echo ERROR: Make not found on PATH & exit /b 1)
where git >nul 2>nul || (echo ERROR: Git not found on PATH & exit /b 1)

if not exist .venv (
    echo Creating virtual environment...
    python -m venv .venv
)
call .venv\Scripts\activate.bat
python -m pip install --upgrade pip
pip install -e ".[dev]"

if not exist .env (
    copy .env.example .env
    echo Created .env from .env.example
)

set PYTHONPATH=%CD%

echo Starting Docker Compose services...
docker compose up -d
timeout /t 10 /nobreak >nul

make migrate
make lint
make typecheck
make test

echo.
echo Setup complete. Run run.bat or make dev to start the API.
endlocal
