"""
Тесты для модуля file_readers.
"""

from unittest.mock import patch

import pandas as pd
import pytest

from src.file_readers import read_csv_file, read_excel_file


@pytest.fixture
def sample_data():
    """Фикстура с образцом данных."""
    return [
        {"id": 1, "amount": 100, "currency": "RUB"},
        {"id": 2, "amount": 200, "currency": "USD"},
    ]


class TestReadCsvFile:
    """Тесты для функции read_csv_file."""

    @patch("src.file_readers.pd.read_csv")
    def test_read_csv_success(self, mock_read_csv, sample_data):
        """Тест успешного чтения CSV."""
        mock_df = pd.DataFrame(sample_data)
        mock_read_csv.return_value = mock_df

        result = read_csv_file("fake.csv")
        assert len(result) == 2
        assert result[0]["id"] == 1
        mock_read_csv.assert_called_once()

    @patch("src.file_readers.pd.read_csv")
    def test_read_csv_empty(self, mock_read_csv):
        """Тест чтения пустого CSV."""
        mock_read_csv.return_value = pd.DataFrame()

        result = read_csv_file("empty.csv")
        assert result == []

    @patch("src.file_readers.pd.read_csv")
    def test_read_csv_file_not_found(self, mock_read_csv):
        """Тест чтения несуществующего файла."""
        mock_read_csv.side_effect = FileNotFoundError()

        result = read_csv_file("nonexistent.csv")
        assert result == []


class TestReadExcelFile:
    """Тесты для функции read_excel_file."""

    @patch("src.file_readers.pd.read_excel")
    def test_read_excel_success(self, mock_read_excel, sample_data):
        """Тест успешного чтения Excel."""
        mock_df = pd.DataFrame(sample_data)
        mock_read_excel.return_value = mock_df

        result = read_excel_file("fake.xlsx")
        assert len(result) == 2
        assert result[0]["id"] == 1
        mock_read_excel.assert_called_once()

    @patch("src.file_readers.pd.read_excel")
    def test_read_excel_empty(self, mock_read_excel):
        """Тест чтения пустого Excel."""
        mock_read_excel.return_value = pd.DataFrame()

        result = read_excel_file("empty.xlsx")
        assert result == []

    @patch("src.file_readers.pd.read_excel")
    def test_read_excel_file_not_found(self, mock_read_excel):
        """Тест чтения несуществующего Excel."""
        mock_read_excel.side_effect = FileNotFoundError()

        result = read_excel_file("nonexistent.xlsx")
        assert result == []
