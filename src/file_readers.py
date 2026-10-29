"""
Модуль для чтения финансовых операций из CSV и Excel файлов.
"""

from typing import Any, Dict, List, cast

import pandas as pd


def read_csv_file(file_path: str) -> List[Dict[str, Any]]:
    """
    Читает CSV-файл с финансовыми операциями.

    Аргументы:
        file_path (str): Путь к CSV-файлу.

    Возвращает:
        List[Dict[str, Any]]: Список словарей с транзакциями.
            Если файл не найден или пустой — возвращает пустой список.
    """
    try:
        df = pd.read_csv(file_path, encoding="utf-8")
        if df.empty:
            return []
        return cast(List[Dict[str, Any]], df.to_dict(orient="records"))
    except (FileNotFoundError, pd.errors.EmptyDataError, Exception):
        return []


def read_excel_file(file_path: str) -> List[Dict[str, Any]]:
    """
    Читает Excel-файл с финансовыми операциями.

    Аргументы:
        file_path (str): Путь к Excel-файлу.

    Возвращает:
        List[Dict[str, Any]]: Список словарей с транзакциями.
            Если файл не найден или пустой — возвращает пустой список.
    """
    try:
        df = pd.read_excel(file_path, engine="openpyxl")
        if df.empty:
            return []
        return cast(List[Dict[str, Any]], df.to_dict(orient="records"))
    except (FileNotFoundError, Exception):
        return []
