# apps/api/Dockerfile
FROM python:3.12-slim AS builder
WORKDIR /build
COPY pyproject.toml README.md ./
COPY apps apps
COPY packages packages
RUN pip install --no-cache-dir --upgrade pip \
 && pip install --no-cache-dir .

FROM python:3.12-slim AS runner
WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends curl \
 && rm -rf /var/lib/apt/lists/* \
 && useradd --create-home --uid 1000 app

# Copy full minor-version lib tree so patch-level image drift does not break site-packages paths.
COPY --from=builder /usr/local/lib/python3.12 /usr/local/lib/python3.12
COPY --from=builder /usr/local/bin /usr/local/bin
COPY --from=builder /build/apps /app/apps
COPY --from=builder /build/packages /app/packages

USER app
ENV PYTHONPATH=/app
EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=15s --retries=3 \
  CMD curl -fsS http://127.0.0.1:8000/health >/dev/null || exit 1

CMD ["python", "-m", "uvicorn", "apps.api.src.main:app", "--host", "0.0.0.0", "--port", "8000"]
