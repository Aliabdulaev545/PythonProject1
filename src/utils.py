"""
Модуль с утилитами для чтения данных.
"""

import json
from typing import Any, Dict, List


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
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        # Проверяем, что данные — это список
        if not isinstance(data, list):
            return []

        # Проверяем, что все элементы — словари
        if not all(isinstance(item, dict) for item in data):
            return []

        return data

    except (FileNotFoundError, json.JSONDecodeError, PermissionError):
        return []
