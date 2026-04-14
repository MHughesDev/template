# apps/api/tests/test_tenancy.py
"""Tenancy-related smoke tests (extend when tenant-scoped resources exist)."""

from __future__ import annotations

import pytest


@pytest.mark.skip(reason="Tenant-scoped resources are not implemented in the template API yet.")
def test_tenant_isolation_placeholder() -> None:
    assert True
