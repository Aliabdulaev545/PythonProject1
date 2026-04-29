"""
Модуль с функциями для работы с виджетом банковских операции.
"""


from src.masks import get_mask_account, get_mask_card_number


def mask_account_card(account_card_info: str) -> str:
    """
    Принимает строку с типом и номером карты или счета ,
    возвращает строку с замаскированным номером.
    """

    parts = account_card_info.rsplit(' ', 1)

    if len(parts) != 2:
        return "Неверный формат ввода"

    card_type = parts[0]
    number = parts[1]

    if card_type.lower() == "счет":
        masked_number = get_mask_account(number)
    else:
        masked_number = get_mask_card_number(number)

    return f"{card_type} {masked_number}"


def get_date(date_string: str) -> str:
    """
    Принимает строку с датой в формате "2024-03-11T02:26:18.671407"
    и возвращает строку с датой в формате "ДД.ММ.ГГГГ".
    """
    date_part = date_string.split('T')[0]
    year, month, day = date_part.split('-')
    return f"{day}.{month}.{year}"
