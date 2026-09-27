from __future__ import annotations

from datetime import datetime


def is_submission_expired(evaluated_at: datetime, submission_deadline: datetime) -> bool:
    return evaluated_at > submission_deadline
