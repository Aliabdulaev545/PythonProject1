"""
Тесты для модуля external_api.
"""

from unittest.mock import Mock, patch

import pytest

from src.external_api import convert_to_rub


class TestConvertToRub:
    """Тесты для функции convert_to_rub."""

    def test_convert_rub_returns_amount(self):
        """Тест: транзакция в RUB возвращает сумму как есть."""
        transaction = {
            "operationAmount": {
                "amount": "1000.50",
                "currency": {"name": "руб.", "code": "RUB"},
            }
        }
        result = convert_to_rub(transaction)
        assert result == 1000.50

    @patch("src.external_api.API_KEY", "test_api_key")
    @patch("src.external_api.requests.get")
    def test_convert_usd_to_rub(self, mock_get):
        """Тест: транзакция в USD конвертируется в RUB."""
        mock_response = Mock()
        mock_response.json.return_value = {"result": 9000.0}
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        transaction = {
            "operationAmount": {
                "amount": "100.0",
                "currency": {"name": "USD", "code": "USD"},
            }
        }
        result = convert_to_rub(transaction)

        assert result == 9000.0
        mock_get.assert_called_once()

    @patch("src.external_api.API_KEY", "test_api_key")
    @patch("src.external_api.requests.get")
    def test_convert_eur_to_rub(self, mock_get):
        """Тест: транзакция в EUR конвертируется в RUB."""
        mock_response = Mock()
        mock_response.json.return_value = {"result": 10000.0}
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        transaction = {
            "operationAmount": {
                "amount": "100.0",
                "currency": {"name": "EUR", "code": "EUR"},
            }
        }
        result = convert_to_rub(transaction)

        assert result == 10000.0

    @patch("src.external_api.API_KEY", None)
    def test_convert_usd_without_api_key(self):
        """Тест: ошибка при отсутствии API-ключа."""
        transaction = {
            "operationAmount": {
                "amount": "100.0",
                "currency": {"name": "USD", "code": "USD"},
            }
        }
        with pytest.raises(ValueError, match="API key not found"):
            convert_to_rub(transaction)

    def test_convert_unknown_currency_returns_amount(self):
        """Тест: неизвестная валюта возвращает сумму как есть."""
        transaction = {
            "operationAmount": {
                "amount": "100.0",
                "currency": {"name": "GBP", "code": "GBP"},
            }
        }
        result = convert_to_rub(transaction)
        assert result == 100.0
