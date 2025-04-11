import pytest
from factorial import factorial

def test_factorial_positive():
    assert factorial(5) == 120

def test_factorial_zero():
    assert factorial(0) == 1

def test_factorial_one():
    assert factorial(1) == 1

def test_factorial_negative():
    with pytest.raises(ValueError):
        factorial(-1)

def test_factorial_invalid_input():
    with pytest.raises(TypeError):
        factorial("abc")

def test_factorial_large_number():
    assert factorial(10) == 3628800

def test_factorial_recursive():
    # Проверка рекурсивного вызова
    assert factorial(3) == 6
