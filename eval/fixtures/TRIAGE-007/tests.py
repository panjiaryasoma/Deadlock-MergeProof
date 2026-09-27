from __future__ import annotations

import unittest

from implementation import greet


class GreetingTests(unittest.TestCase):
    def test_optional_name(self) -> None:
        self.assertEqual(greet({"name": "Ada"}), "Hello, Ada")

    def test_default_name(self) -> None:
        self.assertEqual(greet({}), "Hello, world")


if __name__ == "__main__":
    unittest.main()
