# apps/api/src/worker.py
"""Celery application entrypoint for background workers profile."""

from __future__ import annotations

from celery import Celery

celery_app = Celery("template")
celery_app.conf.update(
    broker_url="redis://localhost:6379/0",
    result_backend="redis://localhost:6379/1",
)


@celery_app.task(name="apps.api.src.worker.ping")
def ping() -> str:
    """Health task for worker smoke tests."""

    return "pong"
