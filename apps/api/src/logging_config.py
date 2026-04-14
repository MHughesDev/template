# apps/api/src/logging_config.py
"""Configure logging from Settings: levels, JSON/text, sensitive field masking."""

from __future__ import annotations

import json
import logging
import sys
from logging import LogRecord
from typing import Any

from apps.api.src.config import Settings

_SENSITIVE_KEYS = frozenset({"password", "secret", "token"})


class JSONFormatter(logging.Formatter):
    """JSON lines with optional ``correlation_id`` from the log record."""

    def format(self, record: LogRecord) -> str:
        payload: dict[str, Any] = {
            "timestamp": self.formatTime(record, self.datefmt),
            "level": record.levelname,
            "message": record.getMessage(),
            "logger": record.name,
        }
        cid = getattr(record, "correlation_id", None)
        if cid is not None:
            payload["correlation_id"] = cid
        for key, value in record.__dict__.items():
            if key.startswith("_") or key in payload:
                continue
            if key in (
                "msg",
                "args",
                "created",
                "msecs",
                "relativeCreated",
                "levelno",
                "levelname",
                "name",
                "pathname",
                "filename",
                "module",
                "exc_info",
                "exc_text",
                "stack_info",
                "lineno",
                "funcName",
                "process",
                "processName",
                "thread",
                "threadName",
                "taskName",
            ):
                continue
            lk = key.lower()
            if any(s in lk for s in _SENSITIVE_KEYS):
                payload[key] = "***REDACTED***"
            else:
                payload[key] = value
        return json.dumps(payload, default=str)


def configure_logging(settings: Settings) -> None:
    """Apply root logging configuration from ``settings``."""

    root = logging.getLogger()
    root.handlers.clear()
    root.setLevel(getattr(logging, settings.log_level.upper(), logging.INFO))

    handler = logging.StreamHandler(sys.stdout)
    if settings.log_format.lower() == "json":
        handler.setFormatter(JSONFormatter())
    else:
        handler.setFormatter(
            logging.Formatter(
                fmt="%(asctime)s %(levelname)s %(name)s %(message)s",
                datefmt="%Y-%m-%dT%H:%M:%S",
            )
        )
    root.addHandler(handler)

    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    sa_level = logging.INFO if settings.api_debug else logging.WARNING
    logging.getLogger("sqlalchemy.engine").setLevel(sa_level)
