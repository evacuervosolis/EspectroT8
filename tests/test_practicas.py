import pytest 
from practicas.functions import is_prime

@pytest.mark.parametrize("number, expected", [
    (1, False),
    (2, True),
    (3, True),
    (4, False),
    (5, True),
    (6, False),
    (7, True),
    (9, False),
    (11, True),
])
def test_is_prime(number, expected):
    assert is_prime(number) == expected