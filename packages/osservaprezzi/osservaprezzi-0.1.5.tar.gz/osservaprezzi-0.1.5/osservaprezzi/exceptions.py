"""Osservaprezzi client exception module."""

from __future__ import annotations


class OsservaprezziError(Exception):
    """Osservaprezzi error."""


class ApiError(OsservaprezziError):
    """Api error."""


class ApiTimeoutError(OsservaprezziError):
    """Api timeout error."""
