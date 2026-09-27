from __future__ import annotations

import unittest

from implementation import accepts_create_user


class CreateUserTests(unittest.TestCase):
    def test_complete_payload_is_accepted(self) -> None:
        self.assertTrue(accepts_create_user({"name": "Ada", "email": "ada@example.test"}))


if __name__ == "__main__":
    unittest.main()
