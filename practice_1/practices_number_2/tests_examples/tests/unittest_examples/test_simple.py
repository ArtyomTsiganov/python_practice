# command to run python -m unittest unittest_examples/test.py
from unittest import TestCase
from tests_examples.main.code import square_it


class TestDemo(TestCase):
    def test_some(self):
        print("simple test")


class TestSquare(TestCase):
    def test_square_it(self):
        #assert 9 == square_it(2)
        self.assertEqual(9, square_it(3))

    def test_square_it_type_error(self):
        self.assertRaises(TypeError, square_it, 3.0)
