import math


def add(a: float, b: float) -> float:
    return a + b


def subtract(x: float, y: float) -> float:
    return x - y


def multiply(x: float, y: float) -> float:
    return x * y


def divide(x: float, y: float) -> float:
    if y == 0:
        raise ZeroDivisionError("Деление на ноль невозможно")
    return x / y


def calculate_logarithm(number: float) -> float:
    if number <= 0:
        raise ValueError("Логарифм можно вычислить только для положительных чисел")
    return math.log(number)


def reverse_string(string: str) -> str:
    return string[::-1]
