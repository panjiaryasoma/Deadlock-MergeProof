from __future__ import annotations

import unittest
from datetime import UTC, datetime, timedelta

from implementation import request_is_valid


class RequestValidityTests(unittest.TestCase):
    def setUp(self) -> None:
        self.deadline = datetime(2026, 9, 27, 12, 0, tzinfo=UTC)

    def test_before_deadline_is_valid(self) -> None:
        self.assertTrue(request_is_valid(self.deadline - timedelta(seconds=1), self.deadline))

    def test_after_deadline_is_invalid(self) -> None:
        self.assertFalse(request_is_valid(self.deadline + timedelta(seconds=1), self.deadline))


if __name__ == "__main__":
    unittest.main()
