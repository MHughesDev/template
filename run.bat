REM run.bat
REM BLUEPRINT: Composer 2 implements from this structure
REM PURPOSE: Windows day-to-day dev runner. Equivalent to run.sh for Windows cmd.exe.
REM          Per spec §10.3 and §26.12 item 350.
REM EQUIVALENT TO: run.sh (same steps, Windows syntax)

REM STEP 1: @echo off and setlocal

REM STEP 2: Verify .env exists
REM   - if not exist .env (echo No .env file. Run setup.bat first. && exit /b 1)

REM STEP 3: Verify .venv exists
REM   - if not exist .venv (echo No .venv. Run setup.bat first. && exit /b 1)

REM STEP 4: Activate .venv
REM   - call .venv\Scripts\activate.bat

REM STEP 5: Start Docker Compose services if not running
REM   - docker compose up -d db
REM   - timeout /t 5 /nobreak

REM STEP 6: Print local URL and key endpoints
REM   - echo API: http://localhost:8000
REM   - echo Docs: http://localhost:8000/docs
REM   - echo Health: http://localhost:8000/health

REM STEP 7: Start API with hot reload
REM   - make dev

REM ERROR HANDLING: if errorlevel 1 at each step, print hint and exit /b 1
