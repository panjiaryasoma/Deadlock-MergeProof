from __future__ import annotations

from datetime import datetime, timedelta, timezone

from demo.src.deadline import is_submission_expired


def _status(evaluated_at: datetime, deadline: datetime) -> str:
    return "EXPIRED" if is_submission_expired(evaluated_at, deadline) else "OPEN"


def main() -> int:
    deadline = datetime(2026, 9, 27, 12, 0, tzinfo=timezone.utc)
    samples = (
        deadline - timedelta(seconds=1),
        deadline + timedelta(seconds=1),
    )

    for evaluated_at in samples:
        print(
            f"evaluated_at={evaluated_at.isoformat()} "
            f"deadline={deadline.isoformat()} status={_status(evaluated_at, deadline)}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
