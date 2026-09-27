from __future__ import annotations

import unittest
from datetime import UTC, datetime, timedelta

from implementation import is_submission_expired


class DeadlineTests(unittest.TestCase):
    def setUp(self) -> None:
        self.deadline = datetime(2026, 9, 27, 12, 0, tzinfo=UTC)

    def test_before_deadline_is_open(self) -> None:
        self.assertFalse(is_submission_expired(self.deadline - timedelta(seconds=1), self.deadline))

    def test_after_deadline_is_expired(self) -> None:
        self.assertTrue(is_submission_expired(self.deadline + timedelta(seconds=1), self.deadline))


if __name__ == "__main__":
    unittest.main()
