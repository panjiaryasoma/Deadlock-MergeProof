from __future__ import annotations


def _canonicalize(value: str) -> str:
    return value.strip().lower()


def normalize_name(value: str) -> str:
    return _canonicalize(value)
