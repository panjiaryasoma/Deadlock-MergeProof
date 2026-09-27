from __future__ import annotations

from datetime import datetime


def request_is_valid(evaluated_at: datetime, deadline: datetime) -> bool:
    return evaluated_at < deadline
