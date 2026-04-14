# docs/troubleshooting/common-issues.md

<!-- BLUEPRINT: Composer 2 implements from this structure -->
<!-- Per spec §26.12 item 377 -->

> PURPOSE: Common development issues and solutions. Per spec §26.12 item 377.

## Port Conflicts

> CONTENT: Port 8000 already in use → change API_PORT in .env. Port 5432 in use → change DB port in docker-compose.yml or stop conflicting service.

## Docker Issues

> CONTENT: Docker not running → start Docker Desktop or `sudo systemctl start docker`. Permission errors → add user to docker group.

## Migration Failures

> CONTENT: Alembic revision not found → run `make db:reset`. Conflict in migration history → check `alembic history`.

## CI Drift (docs:check failing)

> CONTENT: Generated docs out of sync → run `make docs:generate` and commit the result.

## Python Version Issues

> CONTENT: Wrong Python version → use pyenv/asdf: `pyenv install 3.12` then `pyenv local 3.12`.

## Pre-commit Hook Failures

> CONTENT: detect-secrets false positive → run `detect-secrets scan > .secrets.baseline && git add .secrets.baseline`.
