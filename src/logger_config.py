"""
Модуль с настройками логирования.
"""

import logging
import os
from logging import FileHandler, Formatter, Logger


def setup_logger(module_name: str) -> Logger:
    """
    Создаёт и настраивает логер для указанного модуля.

    Аргументы:
        module_name (str): Имя модуля (например, 'utils', 'masks').

    Возвращает:
        Logger: Настроенный объект логера.

    Логи записываются в файл logs/{module_name}.log.
    Формат: метка времени, имя модуля, уровень, сообщение.
    """
    # Создать папку logs, если её нет
    os.makedirs("logs", exist_ok=True)

    # Создать логер
    logger = logging.getLogger(module_name)
    logger.setLevel(logging.DEBUG)

    # Если у логера уже есть handlers — не добавлять повторно
    if logger.handlers:
        return logger

    # Настроить file_handler
    log_file = os.path.join("logs", f"{module_name}.log")
    file_handler = FileHandler(log_file, mode="w", encoding="utf-8")

    # Настроить file_formatter
    file_formatter = Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    file_handler.setFormatter(file_formatter)

    # Установить уровень для handler
    file_handler.setLevel(logging.DEBUG)

    # Добавить handler к логеру
    logger.addHandler(file_handler)

    return logger
