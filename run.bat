@echo off
REM run.bat — start API (uses venv if present)
setlocal
cd /d "%~dp0"
if not exist .env (
  echo No .env — run setup.bat first
  exit /b 1
)
if exist .venv\Scripts\activate.bat call .venv\Scripts\activate.bat
set PYTHONPATH=%CD%

echo Starting Docker services if not running...
docker compose up -d 2>nul
timeout /t 3 /nobreak >nul

echo API: http://localhost:8000
echo Docs: http://localhost:8000/docs

python -m uvicorn apps.api.src.main:app --reload --host 0.0.0.0 --port 8000
endlocal
