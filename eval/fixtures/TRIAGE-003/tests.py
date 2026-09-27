from __future__ import annotations

import unittest

from implementation import normalize_name


class NormalizeNameTests(unittest.TestCase):
    def test_public_behavior_is_unchanged(self) -> None:
        self.assertEqual(normalize_name("  Ada Lovelace  "), "ada lovelace")


if __name__ == "__main__":
    unittest.main()
