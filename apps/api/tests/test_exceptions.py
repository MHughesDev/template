# apps/api/tests/test_exceptions.py
"""Tests for the domain exception hierarchy."""

from __future__ import annotations

import inspect

import pytest

from apps.api.src import exceptions as exc_mod
from apps.api.src.exceptions import (
    AppError,
    AuthenticationError,
    AuthorizationError,
    ConflictError,
    ExternalServiceError,
    NotFoundError,
    RateLimitError,
    StateTransitionError,
    TenantIsolationError,
    ValidationError,
)


def _concrete_exception_classes() -> list[type[AppError]]:
    """All ``AppError`` subclasses defined in ``exceptions`` (excluding AppError)."""

    out: list[type[AppError]] = []
    for name, obj in inspect.getmembers(exc_mod, inspect.isclass):
        if obj is AppError:
            continue
        if issubclass(obj, AppError) and obj.__module__ == exc_mod.__name__:
            out.append(obj)
    return sorted(out, key=lambda c: c.__name__)


def test_app_error_defaults() -> None:
    err = AppError()
    assert err.code == "APP_ERROR"
    assert err.status_code == 500
    assert isinstance(err.message, str) and len(err.message) > 0


def test_app_error_custom_message() -> None:
    err = AppError("custom")
    assert err.message == "custom"


def test_app_error_to_dict() -> None:
    err = AppError("x", detail={"a": 1})
    d = err.to_dict()
    assert d["code"] == "APP_ERROR"
    assert d["message"] == "x"
    assert d["detail"] == {"a": 1}


def test_not_found_error() -> None:
    err = NotFoundError("User", "abc-123")
    assert err.status_code == 404
    assert "User" in err.message and "abc-123" in err.message


def test_tenant_isolation_error() -> None:
    err = TenantIsolationError(
        tenant_id="t1",
        attempted_resource="/api/v1/x",
    )
    assert err.tenant_id == "t1"
    assert err.attempted_resource == "/api/v1/x"


def test_state_transition_error() -> None:
    err = StateTransitionError("draft", "paid", {"draft", "cancelled"})
    assert err.current_state == "draft"
    assert err.attempted_state == "paid"
    assert err.allowed_states == {"draft", "cancelled"}
    assert "draft" in err.message and "paid" in err.message


def test_external_service_error() -> None:
    orig = ValueError("upstream")
    err = ExternalServiceError("stripe", original_error=orig)
    assert err.service_name == "stripe"
    assert err.original_error is orig


def test_rate_limit_error() -> None:
    err = RateLimitError(retry_after=30)
    assert err.retry_after == 30


@pytest.mark.parametrize(
    "cls",
    [
        AppError,
        NotFoundError,
        AuthenticationError,
        AuthorizationError,
        ConflictError,
        ValidationError,
        ExternalServiceError,
        RateLimitError,
        TenantIsolationError,
        StateTransitionError,
    ],
)
def test_all_exceptions_inherit_from_app_error(cls: type[AppError]) -> None:
    assert issubclass(cls, AppError)


def test_all_exceptions_have_unique_codes() -> None:
    codes: list[str] = []
    for cls in _concrete_exception_classes():
        code = getattr(cls, "code", None)
        assert isinstance(code, str), f"{cls.__name__} missing code"
        codes.append(code)
    assert len(codes) == len(set(codes)), f"duplicate codes: {codes}"
