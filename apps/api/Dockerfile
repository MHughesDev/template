# apps/api/Dockerfile
# Container image for the FastAPI API (non-root, healthcheck).

FROM python:3.12-slim

RUN apt-get update \
    && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/*

RUN groupadd --gid 1000 apiuser \
    && useradd --uid 1000 --gid 1000 --no-create-home apiuser

WORKDIR /app

COPY pyproject.toml README.md ./
COPY apps apps
COPY packages packages

RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir .

USER apiuser
EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=10s --start-period=15s --retries=3 \
  CMD curl -fsS http://127.0.0.1:8000/health || exit 1

CMD ["uvicorn", "apps.api.src.main:app", "--host", "0.0.0.0", "--port", "8000"]
