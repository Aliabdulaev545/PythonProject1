"""
Тесты для модуля decorators.
"""

import os
import tempfile

import pytest
from src.decorators import log


# ==================== ФИКСТУРЫ ====================

@pytest.fixture
def temp_log_file():
    """Фикстура для создания временного файла логов."""
    with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', delete=False) as f:
        temp_file = f.name
    yield temp_file
    # Удаляем файл после теста
    if os.path.exists(temp_file):
        os.remove(temp_file)


# ==================== ТЕСТЫ ====================

class TestLogDecorator:
    """Тесты для декоратора log."""

    def test_log_to_console_success(self, capsys):
        """Тест логирования успешного выполнения в консоль."""
        @log()
        def add(a: int, b: int) -> int:
            return a + b

        result = add(3, 5)
        assert result == 8

        captured = capsys.readouterr()
        assert captured.out == "add ok\n"
        assert captured.err == ""

    def test_log_to_console_error(self, capsys):
        """Тест логирования ошибки в консоль."""
        @log()
        def divide(a: int, b: int) -> float:
            return a / b

        with pytest.raises(ZeroDivisionError):
            divide(10, 0)

        captured = capsys.readouterr()
        expected = (
            "divide error: ZeroDivisionError. Inputs: (10, 0), {}\n"
        )
        assert captured.out == expected
        assert captured.err == ""

    def test_log_to_file_success(self, temp_log_file):
        """Тест логирования успешного выполнения в файл."""
        @log(filename=temp_log_file)
        def multiply(a: int, b: int) -> int:
            return a * b

        result = multiply(4, 7)
        assert result == 28

        with open(temp_log_file, 'r', encoding='utf-8') as f:
            content = f.read()
        assert content == "multiply ok\n"

    def test_log_to_file_error(self, temp_log_file):
        """Тест логирования ошибки в файл."""
        @log(filename=temp_log_file)
        def faulty_function(data: list) -> None:
            return data[10]  # IndexError

        with pytest.raises(IndexError):
            faulty_function([1, 2, 3])

        with open(temp_log_file, 'r', encoding='utf-8') as f:
            content = f.read()

        expected = (
            "faulty_function error: IndexError. "
            "Inputs: ([1, 2, 3],), {}\n"
        )
        assert content == expected

    def test_log_with_kwargs(self, capsys):
        """Тест логирования с именованными аргументами."""
        @log()
        def greet(name: str, age: int = 30) -> str:
            return f"Hello, {name}!"

        result = greet(name="Alice", age=25)
        assert result == "Hello, Alice!"

        captured = capsys.readouterr()
        assert captured.out == "greet ok\n"

    def test_log_preserves_function_metadata(self):
        """Тест сохранения метаданных функции декоратором."""
        @log()
        def test_func():
            """Test docstring."""
            pass

        assert test_func.__name__ == "test_func"
        assert test_func.__doc__ == "Test docstring."

    def test_log_with_nested_functions(self, capsys):
        """Тест логирования вложенных функций."""
        @log()
        def outer():
            @log()
            def inner():
                return 42
            return inner()

        result = outer()
        assert result == 42

        captured = capsys.readouterr()
        # Проверяем, что обе функции залогированы
        assert "outer ok\n" in captured.out
        assert "inner ok\n" in captured.out

    def test_log_to_file_with_directory(self):
        """Тест создания директории для логов."""
        log_dir = tempfile.mkdtemp()
        log_file = os.path.join(log_dir, "logs", "test.log")

        @log(filename=log_file)
        def test_func():
            return "Hello"

        test_func()

        assert os.path.exists(log_file)
        with open(log_file, 'r', encoding='utf-8') as f:
            content = f.read()
        assert content == "test_func ok\n"

        # Очистка
        import shutil
        shutil.rmtree(log_dir)
