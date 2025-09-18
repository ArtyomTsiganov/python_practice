# command to run python -m pytest pytest_examples/test.py
import pytest

from tests_examples.main.code import square_it


def test_some():
    print("simple test")


def test_square_it():
    assert square_it(3) == 9


def test_square_it_type_error():
    with pytest.raises(TypeError):
        square_it(3.0)
