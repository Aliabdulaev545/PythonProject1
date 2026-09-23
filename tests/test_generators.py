"""
Тесты для модуля generators.
"""

import pytest

from src.generators import (
    card_number_generator,
    filter_by_currency,
    transaction_descriptions,
)


@pytest.fixture
def sample_transactions():
    """Фикстура с образцом транзакций для тестирования."""
    return [
        {
            "id": 939719570,
            "state": "EXECUTED",
            "date": "2018-06-30T02:08:58.425572",
            "operationAmount": {
                "amount": "9824.07",
                "currency": {"name": "USD", "code": "USD"},
            },
            "description": "Перевод организации",
            "from": "Счет 75106830613657916952",
            "to": "Счет 11776614605963066702",
        },
        {
            "id": 142264268,
            "state": "EXECUTED",
            "date": "2019-04-04T23:20:05.206878",
            "operationAmount": {
                "amount": "79114.93",
                "currency": {"name": "USD", "code": "USD"},
            },
            "description": "Перевод со счета на счет",
            "from": "Счет 19708645243227258542",
            "to": "Счет 75651667383060284188",
        },
        {
            "id": 873106923,
            "state": "EXECUTED",
            "date": "2019-03-23T01:09:46.296404",
            "operationAmount": {
                "amount": "43318.34",
                "currency": {"name": "руб.", "code": "RUB"},
            },
            "description": "Перевод со счета на счет",
            "from": "Счет 44812258784861134719",
            "to": "Счет 74489636417521191160",
        },
        {
            "id": 895315941,
            "state": "EXECUTED",
            "date": "2018-08-19T04:27:37.904916",
            "operationAmount": {
                "amount": "56883.54",
                "currency": {"name": "USD", "code": "USD"},
            },
            "description": "Перевод с карты на карту",
            "from": "Visa Classic 6831982476737658",
            "to": "Visa Platinum 8990922113665229",
        },
        {
            "id": 594226727,
            "state": "CANCELED",
            "date": "2018-09-12T21:27:25.241689",
            "operationAmount": {
                "amount": "67314.70",
                "currency": {"name": "руб.", "code": "RUB"},
            },
            "description": "Перевод организации",
            "from": "Visa Platinum 1246377376343588",
            "to": "Счет 14211924144426031657",
        },
    ]


@pytest.fixture
def empty_transactions():
    """Фикстура с пустым списком транзакций."""
    return []


class TestFilterByCurrency:
    """Тесты для функции filter_by_currency."""

    def test_filter_by_currency_usd(self, sample_transactions):
        """Тест фильтрации транзакций по валюте USD."""
        usd_transactions = list(filter_by_currency(sample_transactions, "USD"))
        assert len(usd_transactions) == 3
        for transaction in usd_transactions:
            assert transaction["operationAmount"]["currency"]["code"] == "USD"

    def test_filter_by_currency_rub(self, sample_transactions):
        """Тест фильтрации транзакций по валюте RUB."""
        rub_transactions = list(filter_by_currency(sample_transactions, "RUB"))
        assert len(rub_transactions) == 2
        for transaction in rub_transactions:
            assert transaction["operationAmount"]["currency"]["code"] == "RUB"

    def test_filter_by_currency_eur_not_found(self, sample_transactions):
        """Тест фильтрации по валюте, которой нет в транзакциях."""
        eur_transactions = list(filter_by_currency(sample_transactions, "EUR"))
        assert len(eur_transactions) == 0

    def test_filter_by_currency_empty_list(self, empty_transactions):
        """Тест фильтрации пустого списка транзакций."""
        result = list(filter_by_currency(empty_transactions, "USD"))
        assert result == []

    def test_filter_by_currency_missing_currency(self):
        """Тест фильтрации транзакций без валюты."""
        transactions = [
            {"id": 1, "operationAmount": {}},
            {"id": 2},
        ]
        result = list(filter_by_currency(transactions, "USD"))
        assert result == []

    @pytest.mark.parametrize("currency_code, expected_count", [
        ("USD", 3),
        ("RUB", 2),
        ("EUR", 0),
    ])
    def test_filter_by_currency_parametrized(
        self, sample_transactions, currency_code, expected_count
    ):
        """Параметризованный тест фильтрации по разным валютам."""
        result = list(filter_by_currency(sample_transactions, currency_code))
        assert len(result) == expected_count


class TestTransactionDescriptions:
    """Тесты для функции transaction_descriptions."""

    def test_transaction_descriptions(self, sample_transactions):
        """Тест получения описаний транзакций."""
        expected = [
            "Перевод организации",
            "Перевод со счета на счет",
            "Перевод со счета на счет",
            "Перевод с карты на карту",
            "Перевод организации",
        ]
        descriptions = list(transaction_descriptions(sample_transactions))
        assert descriptions == expected

    def test_transaction_descriptions_empty_list(self, empty_transactions):
        """Тест получения описаний из пустого списка."""
        descriptions = list(transaction_descriptions(empty_transactions))
        assert descriptions == []

    def test_transaction_descriptions_missing_description(self):
        """Тест получения описаний, когда у транзакции нет описания."""
        transactions = [
            {"id": 1, "description": "Test1"},
            {"id": 2},
            {"id": 3, "description": "Test3"},
        ]
        expected = ["Test1", "Test3"]
        descriptions = list(transaction_descriptions(transactions))
        assert descriptions == expected


class TestCardNumberGenerator:
    """Тесты для генератора card_number_generator."""

    @pytest.mark.parametrize("start, end, expected", [
        (1, 5, [
            "0000 0000 0000 0001",
            "0000 0000 0000 0002",
            "0000 0000 0000 0003",
            "0000 0000 0000 0004",
            "0000 0000 0000 0005",
        ]),
        (9999, 9999, ["0000 0000 0000 9999"]),
        (0, 0, ["0000 0000 0000 0000"]),
    ])
    def test_card_number_generator_parametrized(self, start, end, expected):
        """Параметризованный тест генератора номеров карт."""
        result = list(card_number_generator(start, end))
        assert result == expected

    def test_card_number_generator_formatting(self):
        """Тест правильности форматирования номеров карт."""
        result = list(card_number_generator(1, 3))
        expected = [
            "0000 0000 0000 0001",
            "0000 0000 0000 0002",
            "0000 0000 0000 0003",
        ]
        assert result == expected
        for card in result:
            assert len(card) == 19
            assert card[4] == " "
            assert card[9] == " "
            assert card[14] == " "
