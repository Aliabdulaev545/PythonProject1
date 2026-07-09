"""
Тесты для модуля masks.
"""

import pytest
from src.masks import get_mask_card_number, get_mask_account


# ==================== ФИКСТУРЫ ====================

@pytest.fixture
def valid_card_numbers():
    """Фикстура с валидными номерами карт (16 цифр)"""
    return [
        ("7000792289606361", "7000 79** **** 6361"),
        ("1234567890123456", "1234 56** **** 3456"),
        ("0000000000000000", "0000 00** **** 0000"),
        ("9999999999999999", "9999 99** **** 9999"),
    ]


@pytest.fixture
def edge_card_numbers():
    """Фикстура с граничными случаями номеров карт"""
    return [
        ("123456789012", "1234 56** **** 7890"),  # короткий номер
        ("", "Неверный номер карты"),  # пустая строка
        ("12345", "1234 5",)  # слишком короткий
    ]


@pytest.fixture
def valid_account_numbers():
    """Фикстура с валидными номерами счетов"""
    return [
        ("73654108430135874305", "**4305"),
        ("12345678901234567890", "**7890"),
        ("00000000000000000000", "**0000"),
        ("11112222333344445555", "**5555"),
    ]


@pytest.fixture
def edge_account_numbers():
    """Фикстура с граничными случаями номеров счетов"""
    return [
        ("123", "**123"),  # короткий номер
        ("", "**"),  # пустая строка
        ("12", "**12"),
    ]


# ==================== ТЕСТЫ ДЛЯ get_mask_card_number ====================

class TestGetMaskCardNumber:
    """Тесты для функции get_mask_card_number"""

    @pytest.mark.parametrize("card_number, expected", [
        ("7000792289606361", "7000 79** **** 6361"),
        ("1234567890123456", "1234 56** **** 3456"),
        ("0000000000000000", "0000 00** **** 0000"),
        ("9999999999999999", "9999 99** **** 9999"),
    ])
    def test_mask_card_number_valid(self, card_number, expected):
        """Тест маскировки валидных номеров карт"""
        assert get_mask_card_number(card_number) == expected

    @pytest.mark.parametrize("card_number, expected", [
        ("", "Неверный номер карты"),
        ("12345", "Неверный номер карты"),
        ("123456789012", "Неверный номер карты"),
        ("12345678901234567", "Неверный номер карты"),  # 17 цифр
    ])
    def test_mask_card_number_invalid(self, card_number, expected):
        """Тест маскировки невалидных номеров карт"""
        assert get_mask_card_number(card_number) == expected

    def test_mask_card_number_with_fixture(self, valid_card_numbers):
        """Тест с использованием фикстуры"""
        for card_number, expected in valid_card_numbers:
            assert get_mask_card_number(card_number) == expected


# ==================== ТЕСТЫ ДЛЯ get_mask_account ====================

class TestGetMaskAccount:
    """Тесты для функции get_mask_account"""

    @pytest.mark.parametrize("account_number, expected", [
        ("73654108430135874305", "**4305"),
        ("12345678901234567890", "**7890"),
        ("00000000000000000000", "**0000"),
        ("11112222333344445555", "**5555"),
    ])
    def test_mask_account_valid(self, account_number, expected):
        """Тест маскировки валидных номеров счетов"""
        assert get_mask_account(account_number) == expected

    @pytest.mark.parametrize("account_number, expected", [
        ("", "**"),
        ("123", "**123"),
        ("12", "**12"),
        ("1", "**1"),
    ])
    def test_mask_account_short(self, account_number, expected):
        """Тест маскировки коротких номеров счетов"""
        assert get_mask_account(account_number) == expected

    def test_mask_account_with_fixture(self, valid_account_numbers):
        """Тест с использованием фикстуры"""
        for account_number, expected in valid_account_numbers:
            assert get_mask_account(account_number) == expected
