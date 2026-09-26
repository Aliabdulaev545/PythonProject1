"""
Модуль для работы с внешним API конвертации валют.
"""

import os
from typing import Any, Dict

import requests
from dotenv import load_dotenv

# Загружаем переменные окружения из .env
load_dotenv()

# Получаем токен API из переменных окружения
API_KEY = os.getenv("EXCHANGE_RATES_API_KEY")


def convert_to_rub(transaction: Dict[str, Any]) -> float:
    """
    Конвертирует сумму транзакции в рубли.

    Аргументы:
        transaction (Dict[str, Any]): Словарь с данными о транзакции.

    Возвращает:
        float: Сумма транзакции в рублях.

    Если транзакция была в USD или EUR, происходит обращение
    к внешнему API для получения курса валют.
    """
    # Извлекаем данные о сумме и валюте
    operation_amount = transaction.get("operationAmount", {})
    amount = float(operation_amount.get("amount", 0))
    currency = operation_amount.get("currency", {})
    currency_code = currency.get("code", "RUB")

    # Если валюта RUB — возвращаем сумму как есть
    if currency_code == "RUB":
        return amount

    # Для USD и EUR — конвертируем через API
    if currency_code in ("USD", "EUR"):
        if not API_KEY:
            raise ValueError(
                "API key not found. Set EXCHANGE_RATES_API_KEY in .env file."
            )

        url = "https://api.apilayer.com/exchangerates_data/convert"
        params = {
            "to": "RUB",
            "from": currency_code,
            "amount": amount,
        }
        headers = {"apikey": API_KEY}

        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
        result = response.json()

        return float(result.get("result", 0))

    # Для других валют возвращаем сумму как есть
    return amount
