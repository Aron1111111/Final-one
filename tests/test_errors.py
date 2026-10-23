import unittest
from bookclub.errors import DomainError


class DomainErrorTests(unittest.TestCase):
    def test_preserves_code_and_message(self):
        error = DomainError("EXAMPLE", "Example message")
        self.assertEqual("EXAMPLE", error.code)
        self.assertEqual("Example message", str(error))
        self.assertIsInstance(error, ValueError)
