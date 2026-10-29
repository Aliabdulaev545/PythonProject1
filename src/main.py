"""
Основной модуль программы для работы с банковскими транзакциями.
"""

from typing import Any, Dict, List

from src.file_readers import read_csv_file, read_excel_file
from src.processing import (
    filter_by_state,
    process_bank_search,
    sort_by_date,
)
from src.utils import read_json_file
from src.widget import get_date, mask_account_card


def _load_data(choice: str) -> List[Dict[str, Any]]:
    """Загружает данные в зависимости от выбора пользователя."""
    if choice == "1":
        print("Для обработки выбран JSON-файл.")
        return read_json_file("data/operations.json")
    if choice == "2":
        print("Для обработки выбран CSV-файл.")
        return read_csv_file("data/transactions.csv")
    if choice == "3":
        print("Для обработки выбран XLSX-файл.")
        return read_excel_file("data/transactions_excel.xlsx")
    return []


def _ask_status() -> str:
    """Запрашивает у пользователя статус до корректного ввода."""
    available = ["EXECUTED", "CANCELED", "PENDING"]
    while True:
        print(
            "Введите статус, по которому необходимо выполнить фильтрацию.\n"
            f"Доступные для фильтровки статусы: {', '.join(available)}"
        )
        status = input().strip().upper()
        if status in available:
            print(f'Операции отфильтрованы по статусу "{status}"')
            return status
        print(f'Статус операции "{status}" недоступен.')


def _ask_yes_no(question: str) -> bool:
    """Задаёт вопрос Да/Нет и возвращает bool."""
    while True:
        print(question)
        answer = input().strip().lower()
        if answer in ("да", "yes", "y", "д"):
            return True
        if answer in ("нет", "no", "n", "н"):
            return False
        print("Пожалуйста, ответьте 'Да' или 'Нет'.")


def _print_transactions(transactions: List[Dict[str, Any]]) -> None:
    """Выводит итоговый список транзакций."""
    if not transactions:
        print("Не найдено ни одной транзакции, подходящей под ваши условия фильтрации")
        return

    print("Распечатываю итоговый список транзакций...\n")
    print(f"Всего банковских операций в выборке: {len(transactions)}\n")

    for transaction in transactions:
        date = get_date(transaction.get("date", ""))
        description = transaction.get("description", "")

        # Маскировка отправителя и получателя
        from_acc = transaction.get("from")
        to_acc = transaction.get("to")
        accounts = ""
        if from_acc and to_acc:
            accounts = f"{mask_account_card(from_acc)} -> {mask_account_card(to_acc)}"
        elif to_acc:
            accounts = mask_account_card(to_acc)

        # Сумма и валюта
        operation_amount = transaction.get("operationAmount", {})
        amount = operation_amount.get("amount", "0")
        currency = operation_amount.get("currency", {}).get("name", "")

        print(f"{date} {description}")
        if accounts:
            print(accounts)
        print(f"Сумма: {amount} {currency}\n")


def main() -> None:
    """
    Основная функция программы.

    Запрашивает у пользователя источник данных, статус, сортировку,
    фильтр по валюте и поиск по описанию, затем выводит результат.
    """
    print(
        "Привет! Добро пожаловать в программу работы "
        "с банковскими транзакциями.\n"
        "Выберите необходимый пункт меню:\n"
        "1. Получить информацию о транзакциях из JSON-файла\n"
        "2. Получить информацию о транзакциях из CSV-файла\n"
        "3. Получить информацию о транзакциях из XLSX-файла"
    )

    choice = input().strip()
    transactions = _load_data(choice)

    if not transactions:
        print("Не удалось загрузить данные.")
        return

    status = _ask_status()
    transactions = filter_by_state(transactions, status)

    if _ask_yes_no("Отсортировать операции по дате? Да/Нет"):
        if _ask_yes_no("Отсортировать по возрастанию или по убыванию?"):
            print("Пожалуйста, введите 'по возрастанию' или 'по убыванию'.")
            order = input().strip().lower()
            descending = "убыв" in order
            transactions = sort_by_date(transactions, descending=descending)

    if _ask_yes_no("Выводить только рублевые транзакции? Да/Нет"):
        transactions = [
            t for t in transactions if t.get("operationAmount", {}).get("currency", {}).get("code") == "RUB"
        ]

    if _ask_yes_no("Отфильтровать список транзакций по определенному слову в описании? Да/Нет"):
        print("Введите слово для поиска:")
        word = input().strip()
        transactions = process_bank_search(transactions, word)

    _print_transactions(transactions)


if __name__ == "__main__":
    main()
