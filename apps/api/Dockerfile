# apps/api/Dockerfile
# BLUEPRINT: Composer 2 implements from this structure
# PURPOSE: Multi-stage Docker build for the API. Non-root user, healthcheck,
#          same image used in CI and production. Per spec §26.8 item 207.
# STAGES:
#   - builder: install deps, compile any extensions
#   - runner: minimal runtime, non-root user, HEALTHCHECK, EXPOSE, CMD
# DESIGN DECISIONS:
#   - Non-root user: security requirement (never run as root in container)
#   - HEALTHCHECK: used by Docker Compose and K8s readiness probe
#   - Multi-stage: keeps final image small (no build tools)
#   - Same Dockerfile in CI and production (image:build target)
#   - Python 3.12-slim base: minimal surface area

# STAGE 1: builder
# FROM python:3.12-slim AS builder
# WORKDIR /build
# COPY pyproject.toml ./
# RUN pip install --no-cache-dir build && pip install -e "." (production deps only)
# COPY apps/api/src ./src

# STAGE 2: runner
# FROM python:3.12-slim AS runner
# RUN groupadd --gid 1000 apiuser && useradd --uid 1000 --gid 1000 --no-create-home apiuser
# WORKDIR /app
# COPY --from=builder /build/src ./src
# COPY --from=builder /usr/local/lib/python3.12 /usr/local/lib/python3.12
# USER apiuser
# EXPOSE 8000
# HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
#   CMD curl -f http://localhost:8000/health || exit 1
# CMD ["uvicorn", "apps.api.src.main:app", "--host", "0.0.0.0", "--port", "8000"]
