from __future__ import annotations

from datetime import datetime


def is_submission_expired(
    evaluated_at: datetime,
    submission_deadline: datetime,
) -> bool:
    """Return the current expiration decision for a submission."""
    return evaluated_at > submission_deadline
