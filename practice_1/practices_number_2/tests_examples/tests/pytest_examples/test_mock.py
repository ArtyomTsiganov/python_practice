import pytest
from unittest import mock
from tests_examples.main.code import square_three

def test_mock_vs_magic():
    # Mock — это базовый класс для создания имитаций, а MagicMock
    # — это подкласс Mock, который уже содержит множество предопределенных
    # магических методов
    mocked_instance = mock.Mock()
    magic_instance = mock.MagicMock()

    mocked_instance.__str__ = mock.Mock(return_value="Mock")
    magic_instance.__str__.return_value = "Magic"

    assert str(mocked_instance) == "Mock"
    assert str(magic_instance) == "Magic"

def test_square_three(mocker):
    # don't forger install pytest-mock
    # pip install pytest-mock
    with mocker.patch("tests_examples.main.code.square_it", return_value=144):
        assert square_three() == 144
