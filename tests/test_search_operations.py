"""
Тесты для функций поиска и подсчёта операций.
"""

import pytest

from src.processing import process_bank_operations, process_bank_search


@pytest.fixture
def sample_transactions():
    """Фикстура с образцом транзакций."""
    return [
        {"id": 1, "description": "Перевод организации"},
        {"id": 2, "description": "Перевод со счета на счет"},
        {"id": 3, "description": "Перевод с карты на карту"},
        {"id": 4, "description": "Открытие вклада"},
    ]


class TestProcessBankSearch:
    """Тесты для process_bank_search."""

    def test_search_found(self, sample_transactions):
        """Поиск находит совпадения."""
        result = process_bank_search(sample_transactions, "Перевод")
        assert len(result) == 3

    def test_search_not_found(self, sample_transactions):
        """Поиск не находит совпадений."""
        result = process_bank_search(sample_transactions, "несуществующее")
        assert result == []

    def test_search_case_insensitive(self, sample_transactions):
        """Поиск не зависит от регистра."""
        result = process_bank_search(sample_transactions, "перевод")
        assert len(result) == 3

    def test_search_empty_string(self, sample_transactions):
        """Пустая строка возвращает пустой список."""
        result = process_bank_search(sample_transactions, "")
        assert result == []

    def test_search_missing_description(self):
        """Транзакции без description игнорируются."""
        data = [{"id": 1}, {"id": 2, "description": "Перевод"}]
        result = process_bank_search(data, "Перевод")
        assert len(result) == 1


class TestProcessBankOperations:
    """Тесты для process_bank_operations."""

    def test_count_operations(self, sample_transactions):
        """Подсчёт операций по категориям."""
        categories = ["Перевод организации", "Открытие вклада"]
        result = process_bank_operations(sample_transactions, categories)
        assert result["Перевод организации"] == 1
        assert result["Открытие вклада"] == 1

    def test_count_missing_category(self, sample_transactions):
        """Отсутствующая категория даёт 0."""
        result = process_bank_operations(sample_transactions, ["Несуществующая"])
        assert result["Несуществующая"] == 0

    def test_count_empty_list(self):
        """Пустой список транзакций."""
        result = process_bank_operations([], ["Перевод"])
        assert result == {"Перевод": 0}
