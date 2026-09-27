from __future__ import annotations


def greet(payload: dict[str, object]) -> str:
    name = payload.get("name", "world")
    return f"Hello, {name}"
