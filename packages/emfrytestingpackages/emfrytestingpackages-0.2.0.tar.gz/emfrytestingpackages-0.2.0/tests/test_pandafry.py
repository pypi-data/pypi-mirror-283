# tests/test_module1.py
import unittest
from testingpackages.testingpackages import add_numbers


class TestAddNumbers(unittest.TestCase):
    def test_add_positive_numbers(self):
        self.assertEqual(add_numbers(1, 2), 3)

    def test_add_negative_numbers(self):
        self.assertEqual(add_numbers(-1, -1), -2)

    def test_add_positive_and_negative_numbers(self):
        self.assertEqual(add_numbers(1, -1), 0)

    def test_add_zero(self):
        self.assertEqual(add_numbers(0, 0), 0)
        self.assertEqual(add_numbers(0, 5), 5)
        self.assertEqual(add_numbers(5, 0), 5)


if __name__ == '__main__':
    unittest.main()