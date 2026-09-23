"""
Тесты для модуля processing.
"""

import pytest
from src.processing import filter_by_state, sort_by_date


# ==================== ФИКСТУРЫ ====================

@pytest.fixture
def sample_operations():
    """Фикстура с образцом операций для тестирования"""
    return [
        {'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
        {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'},
        {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
        {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'},
    ]


@pytest.fixture
def all_executed_operations():
    """Фикстура с операциями только статуса EXECUTED"""
    return [
        {'id': 1, 'state': 'EXECUTED', 'date': '2024-01-01T10:00:00'},
        {'id': 2, 'state': 'EXECUTED', 'date': '2024-01-02T10:00:00'},
        {'id': 3, 'state': 'EXECUTED', 'date': '2024-01-03T10:00:00'},
    ]


@pytest.fixture
def all_canceled_operations():
    """Фикстура с операциями только статуса CANCELED"""
    return [
        {'id': 4, 'state': 'CANCELED', 'date': '2024-01-04T10:00:00'},
        {'id': 5, 'state': 'CANCELED', 'date': '2024-01-05T10:00:00'},
    ]


@pytest.fixture
def empty_operations():
    """Фикстура с пустым списком операций"""
    return []


@pytest.fixture
def same_date_operations():
    """Фикстура с операциями, имеющими одинаковую дату"""
    return [
        {'id': 1, 'state': 'EXECUTED', 'date': '2024-01-01T10:00:00'},
        {'id': 2, 'state': 'CANCELED', 'date': '2024-01-01T10:00:00'},
        {'id': 3, 'state': 'PENDING', 'date': '2024-01-01T10:00:00'},
    ]


# ==================== ТЕСТЫ ДЛЯ filter_by_state ====================

class TestFilterByState:
    """Тесты для функции filter_by_state"""

    def test_filter_by_state_default(self, sample_operations):
        """Тест фильтрации по умолчанию (EXECUTED)"""
        result = filter_by_state(sample_operations)
        assert len(result) == 2
        assert all(op['state'] == 'EXECUTED' for op in result)

    @pytest.mark.parametrize("state, expected_count", [
        ('EXECUTED', 2),
        ('CANCELED', 2),
        ('PENDING', 0),
    ])
    def test_filter_by_state_different_states(self, sample_operations, state, expected_count):
        """Параметризованный тест фильтрации по разным статусам"""
        result = filter_by_state(sample_operations, state)
        assert len(result) == expected_count
        if expected_count > 0:
            assert all(op['state'] == state for op in result)

    def test_filter_by_state_all_executed(self, all_executed_operations):
        """Тест фильтрации когда все операции EXECUTED"""
        result = filter_by_state(all_executed_operations, 'EXECUTED')
        assert len(result) == 3
        assert all(op['state'] == 'EXECUTED' for op in result)

    def test_filter_by_state_all_canceled(self, all_canceled_operations):
        """Тест фильтрации когда все операции CANCELED"""
        result = filter_by_state(all_canceled_operations, 'CANCELED')
        assert len(result) == 2
        assert all(op['state'] == 'CANCELED' for op in result)

    def test_filter_by_state_empty_list(self, empty_operations):
        """Тест фильтрации пустого списка"""
        result = filter_by_state(empty_operations)
        assert result == []

    def test_filter_by_state_state_not_found(self, sample_operations):
        """Тест фильтрации по статусу которого нет в списке"""
        result = filter_by_state(sample_operations, 'PENDING')
        assert result == []

    def test_filter_by_state_without_state_key(self):
        """Тест фильтрации когда у операции нет ключа state"""
        operations = [
            {'id': 1, 'date': '2024-01-01'},
            {'id': 2, 'state': 'EXECUTED', 'date': '2024-01-02'},
        ]
        result = filter_by_state(operations, 'EXECUTED')
        assert len(result) == 1
        assert result[0]['id'] == 2


# ==================== ТЕСТЫ ДЛЯ sort_by_date ====================

class TestSortByDate:
    """Тесты для функции sort_by_date"""

    def test_sort_by_date_descending(self, sample_operations):
        """Тест сортировки по убыванию (сначала новые)"""
        result = sort_by_date(sample_operations)
        # Проверяем, что даты идут в порядке убывания
        dates = [op['date'] for op in result]
        assert dates == sorted(dates, reverse=True)

    def test_sort_by_date_ascending(self, sample_operations):
        """Тест сортировки по возрастанию (сначала старые)"""
        result = sort_by_date(sample_operations, descending=False)
        dates = [op['date'] for op in result]
        assert dates == sorted(dates)

    @pytest.mark.parametrize("descending", [True, False])
    def test_sort_by_date_preserves_same_date(self, same_date_operations, descending):
        """Тест сортировки с одинаковыми датами (порядок сохраняется)"""
        result = sort_by_date(same_date_operations, descending)
        # При одинаковых датах порядок элементов должен сохраниться
        assert len(result) == 3
        assert result[0]['id'] == 1
        assert result[1]['id'] == 2
        assert result[2]['id'] == 3

    def test_sort_by_date_empty_list(self, empty_operations):
        """Тест сортировки пустого списка"""
        result = sort_by_date(empty_operations)
        assert result == []

    def test_sort_by_date_single_element(self):
        """Тест сортировки списка с одним элементом"""
        operations = [{'id': 1, 'date': '2024-01-01T10:00:00'}]
        result = sort_by_date(operations)
        assert len(result) == 1
        assert result[0]['id'] == 1

    def test_sort_by_date_invalid_date_format(self):
        """Тест сортировки с некорректным форматом даты"""
        operations = [
            {'id': 1, 'date': 'invalid-date'},
            {'id': 2, 'date': '2024-01-01T10:00:00'},
            {'id': 3, 'date': ''},
        ]
        result = sort_by_date(operations)
        # Функция должна отработать без ошибок
        assert len(result) == 3

    @pytest.mark.parametrize("descending, expected_first_id", [
        (True, 3),   # по убыванию: сначала дата 2024-01-03
        (False, 1),  # по возрастанию: сначала дата 2024-01-01
    ])
    def test_sort_by_date_parametrized(self, descending, expected_first_id):
        """Параметризованный тест сортировки"""
        operations = [
            {'id': 1, 'date': '2024-01-01T10:00:00'},
            {'id': 2, 'date': '2024-01-02T10:00:00'},
            {'id': 3, 'date': '2024-01-03T10:00:00'},
        ]
        result = sort_by_date(operations, descending)
        assert result[0]['id'] == expected_first_id
