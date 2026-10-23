import unittest
from bookclub.description_validator import validate_description
from bookclub.errors import DomainError


class DescriptionValidatorTests(unittest.TestCase):
    def assert_code(self, value, code):
        with self.assertRaises(DomainError) as ctx:
            validate_description(value)
        self.assertEqual(code, ctx.exception.code)

    def test_required(self):
        for value in (None, "", " ", "\t\n"):
            with self.subTest(value=value):
                self.assert_code(value, "DESCRIPTION_REQUIRED")

    def test_rejects_wrong_type(self):
        for value in (7, [], True):
            with self.subTest(value=value):
                self.assert_code(value, "INVALID_DESCRIPTION_TYPE")

    def test_nine_is_too_short(self):
        self.assert_code("a" * 9, "DESCRIPTION_TOO_SHORT")

    def test_ten_is_valid(self):
        self.assertEqual("a" * 10, validate_description("a" * 10))

    def test_thousand_is_valid(self):
        self.assertEqual("a" * 1000, validate_description("a" * 1000))

    def test_thousand_and_one_is_too_long(self):
        self.assert_code("a" * 1001, "DESCRIPTION_TOO_LONG")

    def test_trims_before_counting(self):
        self.assertEqual("a" * 10, validate_description("  " + "a" * 10 + "\n"))
        self.assert_code(" " + "a" * 9 + " ", "DESCRIPTION_TOO_SHORT")

    def test_unicode_code_points(self):
        self.assertEqual("书" * 10, validate_description("书" * 10))
