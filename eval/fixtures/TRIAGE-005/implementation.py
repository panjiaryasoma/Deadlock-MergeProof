from __future__ import annotations


ITEMS = {"known": {"name": "Known item"}}


def get_item_status(item_id: str) -> int:
    return 200 if item_id in ITEMS else 404
