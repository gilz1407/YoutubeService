import pytest


@pytest.mark.critical
def test_subtraction2():
    assert 2 == 4, "The subtraction operation was failed, Expected to 4-2=2"


@pytest.mark.low
def test_multiplication2():
    assert (2 * 2) == 4, "The subtraction operation was failed, Expected to 2*2=4"
