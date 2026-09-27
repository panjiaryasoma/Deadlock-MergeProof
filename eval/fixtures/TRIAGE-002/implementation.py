from __future__ import annotations


def accepts_create_user(payload: dict[str, object]) -> bool:
    return "name" in payload
