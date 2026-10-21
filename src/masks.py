"""
Модуль с функциями маскировки номеров карт и счетов.
"""

from src.logger_config import setup_logger

# Создать логер для модуля masks
logger = setup_logger("masks")


def get_mask_card_number(card_number: str) -> str:
    """
    Маскирует номер банковской карты.

    Формат: "XXXX XX** **** XXXX"

    Аргументы:
        card_number (str): Номер карты (16 цифр).

    Возвращает:
        str: Замаскированный номер карты.
    """
    logger.debug(f"Маскировка карты: {card_number}")

    if len(card_number) != 16:
        logger.error(f"Неверная длина номера карты: {len(card_number)} (ожидается 16)")
        return "Неверный номер карты"

    block1 = card_number[:4]
    block2 = card_number[4:6]
    block4 = card_number[-4:]
    result = f"{block1} {block2}** **** {block4}"

    logger.info(f"Карта успешно замаскирована: {result}")
    return result


def get_mask_account(account_number: str) -> str:
    """
    Маскирует номер банковского счёта.

    Формат: "**XXXX"

    Аргументы:
        account_number (str): Номер счёта (цифры).

    Возвращает:
        str: Замаскированный номер счёта.
    """
    logger.debug(f"Маскировка счёта: {account_number}")

    if len(account_number) < 4:
        logger.error(f"Слишком короткий номер счёта: {len(account_number)} (минимум 4)")
        return f"**{account_number}"

    result = f"**{account_number[-4:]}"
    logger.info(f"Счёт успешно замаскирован: {result}")
    return result
