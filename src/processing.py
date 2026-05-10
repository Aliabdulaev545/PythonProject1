"""
Модуль с функциями обработки данных банковских операций.
"""

from typing import List, Dict, Any


def filter_by_state(operations: List[Dict[str, Any]], state: str = 'EXECUTED') -> List[Dict[str, Any]]:
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
    return [operation for operation in operations if operation.get('state') == state]


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
    return sorted(operations, key=lambda operation: operation.get('date', ''), reverse=descending)
