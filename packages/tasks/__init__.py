# packages/tasks/__init__.py
"""
BLUEPRINT: packages/tasks/__init__.py

PURPOSE:
Package marker. Exports task interfaces for background job submission and handling.
Workers are an optional profile. Per spec §26.9 item 239.
"""

from packages.tasks.interfaces import TaskHandler, TaskInterface

__all__ = ["TaskInterface", "TaskHandler"]
