"""
Модуль с функциями обработки данных банковских операций.
"""

import re
from collections import Counter
from typing import Any, Dict, List


def filter_by_state(operations: List[Dict[str, Any]], state: str = "EXECUTED") -> List[Dict[str, Any]]:
    """
    Фильтрует список операций по значению ключа 'state'.

    Аргументы:
        operations (List[Dict[str, Any]]): Список словарей с данными операций.
        state (str): Значение для фильтрации по ключу 'state'. По умолчанию 'EXECUTED'.

    Возвращает:
        List[Dict[str, Any]]: Новый список словарей, где state соответствует указанному значению.

    Пример:
        >>> operations = [
        ...     {'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
        ...     {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'},
        ...     {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'}
        ... ]
        >>> filter_by_state(operations)
        [
            {'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
            {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'}
        ]
    """
    return [operation for operation in operations if operation.get("state") == state]


def sort_by_date(operations: List[Dict[str, Any]], descending: bool = True) -> List[Dict[str, Any]]:
    """
    Сортирует список операций по дате.

    Аргументы:
        operations (List[Dict[str, Any]]): Список словарей с данными операций.
        descending (bool): Порядок сортировки.
            True - по убыванию (сначала новые), False - по возрастанию.

    Возвращает:
        List[Dict[str, Any]]: Новый отсортированный список операций.

    Пример:
        >>> operations = [
        ...     {'id': 41428829, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'},
        ...     {'id': 939719570, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'}
        ... ]
        >>> sort_by_date(operations)
        [
            {'id': 939719570, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
            {'id': 41428829, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'}
        ]
    """
    return sorted(operations, key=lambda operation: operation.get("date", ""), reverse=descending)


def process_bank_search(data: List[Dict[str, Any]], search: str) -> List[Dict[str, Any]]:
    """
    Ищет транзакции, в описании которых есть заданная строка.

    Аргументы:
        data (List[Dict[str, Any]]): Список словарей с транзакциями.
        search (str): Строка для поиска в описании.

    Возвращает:
        List[Dict[str, Any]]: Список транзакций, где в description
            найдено совпадение с search (без учёта регистра).

    Пример:
        >>> process_bank_search(data, "перевод")
        [{'id': 1, 'description': 'Перевод организации', ...}]
    """
    if not search:
        return []

    pattern = re.compile(re.escape(search), re.IGNORECASE)
    result = []

    for transaction in data:
        description = transaction.get("description", "")
        if isinstance(description, str) and pattern.search(description):
            result.append(transaction)

    return result


def process_bank_operations(data: List[Dict[str, Any]], categories: List[str]) -> Dict[str, int]:
    """
    Подсчитывает количество операций по категориям.

    Аргументы:
        data (List[Dict[str, Any]]): Список словарей с транзакциями.
        categories (List[str]): Список категорий (значений поля description).

    Возвращает:
        Dict[str, int]: Словарь, где ключи — категории,
            значения — количество операций в каждой категории.

    Пример:
        >>> process_bank_operations(data, ["Перевод организации"])
        {'Перевод организации': 2}
    """
    descriptions = [
        transaction.get("description", "") for transaction in data if transaction.get("description") in categories
    ]

    counter = Counter(descriptions)
    return {category: counter.get(category, 0) for category in categories}
