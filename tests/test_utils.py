"""
Тесты для модуля utils.
"""

import json
import os
import tempfile
from unittest.mock import patch, mock_open

import pytest

from src.utils import read_json_file


@pytest.fixture
def temp_json_file():
    """Фикстура для создания временного JSON-файла."""
    with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", suffix=".json", delete=False) as f:
        json.dump([{"id": 1, "amount": 100}], f)
        temp_file = f.name
    yield temp_file
    if os.path.exists(temp_file):
        os.remove(temp_file)


@pytest.fixture
def empty_json_file():
    """Фикстура для создания пустого JSON-файла."""
    with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", suffix=".json", delete=False) as f:
        temp_file = f.name
    yield temp_file
    if os.path.exists(temp_file):
        os.remove(temp_file)


class TestReadJsonFile:
    """Тесты для функции read_json_file."""

    def test_read_valid_json(self, temp_json_file):
        """Тест чтения валидного JSON-файла."""
        result = read_json_file(temp_json_file)
        assert result == [{"id": 1, "amount": 100}]

    def test_read_empty_json(self, empty_json_file):
        """Тест чтения пустого JSON-файла."""
        with open(empty_json_file, "w") as f:
            f.write("")
        result = read_json_file(empty_json_file)
        assert result == []

    def test_read_non_existent_file(self):
        """Тест чтения несуществующего файла."""
        result = read_json_file("nonexistent_file.json")
        assert result == []

    def test_read_json_not_a_list(self):
        """Тест чтения JSON, который не является списком."""
        with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", suffix=".json", delete=False) as f:
            json.dump({"key": "value"}, f)
            temp_file = f.name
        try:
            result = read_json_file(temp_file)
            assert result == []
        finally:
            os.remove(temp_file)

    def test_read_json_invalid_syntax(self):
        """Тест чтения JSON с невалидным синтаксисом."""
        with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", suffix=".json", delete=False) as f:
            f.write("not a valid json")
            temp_file = f.name
        try:
            result = read_json_file(temp_file)
            assert result == []
        finally:
            os.remove(temp_file)

    def test_read_json_with_mock(self):
        """Тест чтения JSON с использованием Mock."""
        mock_data = [{"id": 1, "amount": 100}]
        with patch("builtins.open", mock_open(read_data=json.dumps(mock_data))):
            result = read_json_file("fake_path.json")
            assert result == mock_data
