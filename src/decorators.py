"""
Модуль с декораторами для логирования выполнения функций.
"""

import functools
import os
from typing import Any, Callable, Optional, TypeVar, cast

F = TypeVar('F', bound=Callable[..., Any])


def log(filename: Optional[str] = None) -> Callable[[F], F]:
    """
    Декоратор для логирования выполнения функции.

    Аргументы:
        filename (Optional[str]): Имя файла для записи логов.
            Если не указан, логи выводятся в консоль.

    Возвращает:
        Callable: Декорированная функция.

    Пример:
        @log(filename="mylog.txt")
        def my_function(x, y):
            return x + y

        my_function(1, 2)  # Запишет "my_function ok" в mylog.txt
    """
    def decorator(func: F) -> F:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            try:
                result = func(*args, **kwargs)
                log_message = f"{func.__name__} ok"
                _write_log(log_message, filename)
                return result
            except Exception as e:
                error_message = (
                    f"{func.__name__} error: {type(e).__name__}. "
                    f"Inputs: {args}, {kwargs}"
                )
                _write_log(error_message, filename)
                raise
        return cast(F, wrapper)
    return decorator


def _write_log(message: str, filename: Optional[str] = None) -> None:
    """
    Вспомогательная функция для записи лога в файл или консоль.

    Аргументы:
        message (str): Сообщение для записи.
        filename (Optional[str]): Имя файла для записи.
            Если не указан, сообщение выводится в консоль.
    """
    if filename:
        # Создаём директорию для логов, если её нет
        log_dir = os.path.dirname(filename)
        if log_dir:
            os.makedirs(log_dir, exist_ok=True)
        with open(filename, 'a', encoding='utf-8') as f:
            f.write(message + '\n')
    else:
        print(message)

