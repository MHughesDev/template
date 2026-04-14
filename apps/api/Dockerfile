# apps/api/Dockerfile
# Build from repository root: docker build -f apps/api/Dockerfile .

FROM python:3.14-slim
WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends curl \
  && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml README.md ./
COPY apps apps
COPY packages packages

RUN pip install --no-cache-dir --upgrade pip \
  && pip install --no-cache-dir .

RUN useradd --create-home --uid 1000 app
USER app

ENV PYTHONPATH=/app
EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=15s --retries=3 \
  CMD curl -fsS http://127.0.0.1:8000/health >/dev/null || exit 1

CMD ["python", "-m", "uvicorn", "apps.api.src.main:app", "--host", "0.0.0.0", "--port", "8000"]
