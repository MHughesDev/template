REM setup.bat
REM BLUEPRINT: Composer 2 implements from this structure
REM PURPOSE: Windows one-shot bootstrap after clone. Equivalent to setup.sh for Windows cmd.exe.
REM          Per spec §10.3 and §26.12 item 348.
REM EQUIVALENT TO: setup.sh (same steps, Windows syntax)

REM STEP 1: @echo off and set error handling
REM @echo off
REM setlocal enabledelayedexpansion

REM STEP 2: Print welcome banner

REM STEP 3: Verify prerequisites
REM   - Python 3.12+: python --version | findstr "3.12" || (echo Python 3.12+ required && exit /b 1)
REM   - Docker: docker --version || (echo Docker required && exit /b 1)
REM   - Docker Compose v2: docker compose version || (echo Docker Compose v2 required && exit /b 1)
REM   - Make: make --version || (echo Make required - install via chocolatey: choco install make && exit /b 1)
REM   - Git: git --version || (echo Git required && exit /b 1)

REM STEP 4: Create virtual environment
REM   - python -m venv .venv
REM   - if errorlevel 1 (echo Failed to create .venv && exit /b 1)

REM STEP 5: Activate .venv and install dependencies
REM   - call .venv\Scripts\activate.bat
REM   - pip install --upgrade pip
REM   - pip install -e ".[dev,test,lint]"

REM STEP 6: Copy .env.example to .env if not exists
REM   - if not exist .env (copy .env.example .env && echo Edit .env with your values)

REM STEP 7: Start Docker Compose services
REM   - docker compose up -d db

REM STEP 8: Wait for services and run migrations
REM   - timeout /t 5 /nobreak
REM   - make migrate

REM STEP 9: Run lint and typecheck
REM   - make lint
REM   - make typecheck

REM STEP 10: Run tests
REM   - make test

REM STEP 11: Print success and next steps
REM   - echo Setup complete! Run run.bat to start the dev server.
