__author__ = "Idea belong to Daniil Myasnikov"

from unittest import TestCase, mock
from tests_examples.main.code import square_three


class TestWithMock(TestCase):
    def test_mock_vs_magic(self):
        # Mock — это базовый класс для создания имитаций, а MagicMock
        # — это подкласс Mock, который уже содержит множество предопределенных
        # магических методов
        mocked_instance = mock.Mock()
        magic_instance = mock.MagicMock()

        mocked_instance.__str__ = mock.Mock(return_value="Mock")
        magic_instance.__str__.return_value = "Magic"

        self.assertEqual("Mock", str(mocked_instance))
        self.assertEqual("Magic", str(magic_instance))


class TestWithPatch(TestCase):
    def test_square_three(self):
        with mock.patch("tests_examples.main.code.square_it") as mocked_function:
            mocked_function.return_value = 144 # наше ожидание о возвращаемом значении
            self.assertEqual(144, square_three()) # тогда окажется, что 3 в квадрате это 144

