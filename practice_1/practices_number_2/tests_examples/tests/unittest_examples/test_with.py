from unittest import TestCase
from tests_examples.main.code import square_it


class TestDemo(TestCase):
    def test_some(self):
        print("simple test")


class TestSquare(TestCase):
    def test_square_it(self):
        self.assertEqual(9, square_it(3))

    def test_square_it_type_error(self):
        with self.assertRaises(TypeError) as context:
            square_it(3.0)
        self.assertTrue("something" in str(context.exception))
