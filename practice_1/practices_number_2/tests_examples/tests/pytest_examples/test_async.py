import pytest
from tests_examples.main.code import square_it


class TestDemo:
    @pytest.mark.asyncio
    async def test_some(self):
        print("simple test")


class TestSquare():
    @pytest.mark.asyncio
    async def test_square_it(self):
        assert 9 == square_it(3)

    @pytest.mark.asyncio
    async def test_square_it_type_error(self):
        with pytest.raises(TypeError) as context:
            square_it(3.0)
        assert "something" in str(context.value)
