"""
Тесты для модуля widget.
"""

import pytest
from src.widget import mask_account_card, get_date


# ==================== ФИКСТУРЫ ====================

@pytest.fixture
def card_test_data():
    """Фикстура с данными для тестирования карт"""
    return [
        ("Visa Platinum 7000792289606361", "Visa Platinum 7000 79** **** 6361"),
        ("Maestro 1596837868705199", "Maestro 1596 83** **** 5199"),
        ("MasterCard 7158300734726758", "MasterCard 7158 30** **** 6758"),
        ("Visa Classic 6831982476737658", "Visa Classic 6831 98** **** 7658"),
        ("Visa Gold 5999414228426353", "Visa Gold 5999 41** **** 6353"),
    ]


@pytest.fixture
def account_test_data():
    """Фикстура с данными для тестирования счетов"""
    return [
        ("Счет 73654108430135874305", "Счет **4305"),
        ("Счет 64686473678894779589", "Счет **9589"),
        ("Счет 35383033474447895560", "Счет **5560"),
    ]


@pytest.fixture
def invalid_test_data():
    """Фикстура с некорректными входными данными"""
    return [
        ("Visa Platinum", "Неверный формат ввода"),
        ("", "Неверный формат ввода"),
        ("Счет", "Неверный формат ввода"),
        ("1234567890", "Неверный формат ввода"),
    ]


@pytest.fixture
def date_test_data():
    """Фикстура с датами для тестирования"""
    return [
        ("2024-03-11T02:26:18.671407", "11.03.2024"),
        ("2025-12-25T10:30:00.000000", "25.12.2025"),
        ("2023-01-01T00:00:00.123456", "01.01.2023"),
        ("2024-02-29T15:45:30", "29.02.2024"),  # високосный год
    ]


# ==================== ТЕСТЫ ДЛЯ mask_account_card ====================

class TestMaskAccountCard:
    """Тесты для функции mask_account_card"""

    @pytest.mark.parametrize("input_data, expected", [
        ("Visa Platinum 7000792289606361", "Visa Platinum 7000 79** **** 6361"),
        ("Maestro 1596837868705199", "Maestro 1596 83** **** 5199"),
        ("MasterCard 7158300734726758", "MasterCard 7158 30** **** 6758"),
    ])
    def test_mask_account_card_cards(self, input_data, expected):
        """Тест маскировки различных типов карт"""
        assert mask_account_card(input_data) == expected

    @pytest.mark.parametrize("input_data, expected", [
        ("Счет 73654108430135874305", "Счет **4305"),
        ("Счет 64686473678894779589", "Счет **9589"),
        ("Счет 35383033474447895560", "Счет **5560"),
    ])
    def test_mask_account_card_accounts(self, input_data, expected):
        """Тест маскировки различных счетов"""
        assert mask_account_card(input_data) == expected

    @pytest.mark.parametrize("input_data, expected", [
        ("Visa Platinum", "Неверный формат ввода"),
        ("", "Неверный формат ввода"),
        ("Счет", "Неверный формат ввода"),
        ("1234567890", "Неверный формат ввода"),
    ])
    def test_mask_account_card_invalid(self, input_data, expected):
        """Тест обработки некорректных входных данных"""
        assert mask_account_card(input_data) == expected

    def test_mask_account_card_with_fixture(self, card_test_data):
        """Тест с фикстурой для карт"""
        for input_data, expected in card_test_data:
            assert mask_account_card(input_data) == expected

    def test_mask_account_card_accounts_fixture(self, account_test_data):
        """Тест с фикстурой для счетов"""
        for input_data, expected in account_test_data:
            assert mask_account_card(input_data) == expected


# ==================== ТЕСТЫ ДЛЯ get_date ====================

class TestGetDate:
    """Тесты для функции get_date"""

    @pytest.mark.parametrize("input_date, expected", [
        ("2024-03-11T02:26:18.671407", "11.03.2024"),
        ("2025-12-25T10:30:00.000000", "25.12.2025"),
        ("2023-01-01T00:00:00.123456", "01.01.2023"),
        ("2024-02-29T15:45:30", "29.02.2024"),
    ])
    def test_get_date_valid(self, input_date, expected):
        """Тест преобразования валидных дат"""
        assert get_date(input_date) == expected

    @pytest.mark.parametrize("input_date, expected", [
        ("2024-03-11T02:26:18", "11.03.2024"),  # корректная дата
        ("2024-03-11", "2024-03-11"),  # без времени - возвращаем как есть
        ("", ""),  # пустая строка
    ])
    def test_get_date_edge_cases(self, input_date, expected):
        """Тест граничных случаев преобразования дат"""
        assert get_date(input_date) == expected

    def test_get_date_with_fixture(self, date_test_data):
        """Тест с использованием фикстуры"""
        for input_date, expected in date_test_data:
            assert get_date(input_date) == expected
