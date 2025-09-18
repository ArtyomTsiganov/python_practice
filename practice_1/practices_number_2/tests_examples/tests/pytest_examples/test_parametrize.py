# command to run python -m pytest pytest_examples/test.py
import pytest

from tests_examples.main.code import square_it


def test_some():
    print("simple test")


@pytest.mark.parametrize("input,expected", [
    (3, 9),
    (4, 16),
    (5, 25),
])
def test_square_it(input, expected):
    assert square_it(input) == expected


@pytest.mark.parametrize("input", [
    3.0,
    "string",
    None,
])
def test_square_it_type_error(input):
    with pytest.raises(TypeError):
        square_it(input)
