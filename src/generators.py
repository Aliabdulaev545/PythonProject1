"""
Модуль с генераторами для обработки данных транзакций.
"""

from typing import Any, Dict, Iterator, List


def filter_by_currency(
    transactions: List[Dict[str, Any]], currency_code: str
) -> Iterator[Dict[str, Any]]:
    """
    Генератор, фильтрующий транзакции по заданной валюте.

    Аргументы:
        transactions (List[Dict[str, Any]]): Список словарей с транзакциями.
        currency_code (str): Код валюты для фильтрации (например, 'USD', 'RUB').

    Возвращает:
        Iterator[Dict[str, Any]]: Итератор, выдающий транзакции с указанной валютой.

    Пример:
        >>> transactions = [...]
        >>> usd_transactions = filter_by_currency(transactions, "USD")
        >>> for transaction in usd_transactions:
        ...     print(transaction["operationAmount"]["currency"]["code"])
        USD
        USD
    """
    for transaction in transactions:
        try:
            currency = transaction.get("operationAmount", {}).get("currency", {})
            if currency.get("code") == currency_code:
                yield transaction
        except (KeyError, AttributeError):
            continue


def transaction_descriptions(transactions: List[Dict[str, Any]]) -> Iterator[str]:
    """
    Генератор, выдающий описания транзакций по очереди.

    Аргументы:
        transactions (List[Dict[str, Any]]): Список словарей с транзакциями.

    Возвращает:
        Iterator[str]: Итератор с описаниями транзакций.

    Пример:
        >>> transactions = [...]
        >>> descriptions = transaction_descriptions(transactions)
        >>> for desc in descriptions:
        ...     print(desc)
        Перевод организации
        Перевод со счета на счет
    """
    for transaction in transactions:
        try:
            description = transaction.get("description", "")
            if description:
                yield description
        except (KeyError, AttributeError):
            continue


def card_number_generator(start: int, end: int) -> Iterator[str]:
    """
    Генератор номеров банковских карт в формате "XXXX XXXX XXXX XXXX".

    Аргументы:
        start (int): Начальное значение диапазона (включительно).
        end (int): Конечное значение диапазона (включительно).

    Возвращает:
        Iterator[str]: Итератор с номерами карт в формате "XXXX XXXX XXXX XXXX".

    Пример:
        >>> for card in card_number_generator(1, 5):
        ...     print(card)
        0000 0000 0000 0001
        0000 0000 0000 0002
        0000 0000 0000 0003
        0000 0000 0000 0004
        0000 0000 0000 0005

    Примечание:
        Генератор поддерживает диапазон от 0000 0000 0000 0001 до 9999 9999 9999 9999.
    """
    for number in range(start, end + 1):
        card_number = f"{number:016d}"
        formatted = " ".join(
            [card_number[i:i + 4] for i in range(0, 16, 4)]
        )
        yield formatted
