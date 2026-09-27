from __future__ import annotations

import unittest
from datetime import UTC, datetime, timedelta

from demo.src.deadline import is_submission_expired


class SubmissionDeadlineTests(unittest.TestCase):
    def setUp(self) -> None:
        self.deadline = datetime(2026, 9, 27, 12, 0, tzinfo=UTC)

    def test_before_deadline_is_open(self) -> None:
        evaluated_at = self.deadline - timedelta(seconds=1)

        self.assertFalse(is_submission_expired(evaluated_at, self.deadline))

    def test_after_deadline_is_expired(self) -> None:
        evaluated_at = self.deadline + timedelta(seconds=1)

        self.assertTrue(is_submission_expired(evaluated_at, self.deadline))


if __name__ == "__main__":
    unittest.main()
