from unittest import TestCase
from tests_examples.main.code import square_it


class TestSetUpAndDown(TestCase):
    def setUp(self):
        print("set up")

    def tearDown(self):
        print("set down")

    def test_some(self):
        self.assertEqual(9, square_it(3))

    def test_another(self):
        self.assertEqual(16, square_it(4))
