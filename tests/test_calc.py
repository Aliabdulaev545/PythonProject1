import pytest
from src.calc import add, subtract, multiply, divide, calculate_logarithm


# Тест функции сложения
def test_add():
    assert add(2, 3) == 5
    assert add(-2, 3) == 1
    assert add(0, 0) == 0

# Тест функции вычитания
def test_subtract():
    assert subtract(2, 3) == -1
    assert subtract(-2, 3) == -5
    assert subtract(0, 0) == 0

# Тест функции умножения
def test_multiply():
    assert multiply(2, 3) == 6
    assert multiply(-2, 3) == -6
    assert multiply(0, 0) == 0

# Тест функции деления
def test_divide():
    assert divide(6, 2) == 3
    assert divide(-6, 3) == -2
    assert divide(0, 5) == 0
    with pytest.raises(ZeroDivisionError):
        divide(6, 0)

def test_calculate_logarithm_with_negative_number():
    with pytest.raises(ValueError) as exc_info:
        calculate_logarithm(-1)

    # Проверяем, что сообщение об ошибке соответствует ожидаемому
    assert str(exc_info.value) == "Логарифм можно вычислить только для положительных чисел"