import pytest
from ....tests_examples.main.code import square_it

@pytest.fixture()
def fixture_1():
    print("set up")
    yield
    print("set_down")

@pytest.fixture()
def fixture_2():
    print("fixture 2 setup")


def test_some(fixture_1, fixture_2):
    assert square_it(3) == 9
    print("test some")

def test_another(fixture_2):
    assert square_it(4) == 16
