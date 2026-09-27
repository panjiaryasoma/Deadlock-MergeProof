from __future__ import annotations

import unittest

from implementation import REQUEST_TIMEOUT_SECONDS


class TimeoutConfigurationTests(unittest.TestCase):
    def test_timeout_is_positive(self) -> None:
        self.assertGreater(REQUEST_TIMEOUT_SECONDS, 0)


if __name__ == "__main__":
    unittest.main()
