"""
Модуль с утилитами для чтения данных.
"""

import json
from typing import Any, Dict, List

from src.logger_config import setup_logger

# Создать логер для модуля utils
logger = setup_logger("utils")


def read_json_file(file_path: str) -> List[Dict[str, Any]]:
    """
    Читает JSON-файл и возвращает список словарей с транзакциями.

    Аргументы:
        file_path (str): Путь к JSON-файлу.

    Возвращает:
        List[Dict[str, Any]]: Список словарей с данными о транзакциях.
            Если файл пустой, содержит не список или не найден,
            возвращается пустой список.
    """
    logger.debug(f"Попытка чтения файла: {file_path}")

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        if not isinstance(data, list):
            logger.error(f"Файл {file_path} содержит не список, а {type(data).__name__}")
            return []

        if not all(isinstance(item, dict) for item in data):
            logger.error(f"Файл {file_path} содержит не словари")
            return []

        logger.info(f"Файл {file_path} успешно прочитан. Записей: {len(data)}")
        return data

    except FileNotFoundError:
        logger.error(f"Файл не найден: {file_path}")
        return []
    except json.JSONDecodeError as e:
        logger.error(f"Ошибка декодирования JSON в файле {file_path}: {e}")
        return []
    except PermissionError:
        logger.error(f"Нет доступа к файлу: {file_path}")
        return []
