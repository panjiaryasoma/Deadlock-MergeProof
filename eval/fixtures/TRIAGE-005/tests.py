from __future__ import annotations

import unittest

from implementation import get_item_status


class GetItemTests(unittest.TestCase):
    def test_known_item_returns_200(self) -> None:
        self.assertEqual(get_item_status("known"), 200)


if __name__ == "__main__":
    unittest.main()
