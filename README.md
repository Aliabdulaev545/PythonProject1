# Виджет банковских операций

Проект для бэкенда банка. Готовит данные для виджета с последними успешными операциями клиента.

## Возможности

- Получение последних успешных операций
- Подготовка данных для виджета
- Работа с банковскими транзакциями
- Маскировка номеров карт и счетов
- Фильтрация и сортировка операций по дате и статусу

## Установка и запуск

1. Клонируйте репозиторий:
   ```bash
   git clone git@github.com:Aliabdulaev545/PythonProject1.git
   

2. Установите зависимости:

pip install -r requirements.txt


3. Создайте конфигурационный файл:

cp .env.example .env

## Модули проекта
### Модуль masks
Содержит функции для маскировки номеров карт и счетов.

get_mask_card_number(card_number: str) -> str
Маскирует номер банковской карты в формате "XXXX XX** **** XXXX".

Пример:
from src.masks import get_mask_card_number

masked = get_mask_card_number("7000792289606361")
print(masked)  # 7000 79** **** 6361

get_mask_account(account_number: str) -> str
Маскирует номер банковского счета в формате "**XXXX".

Пример:
from src.masks import get_mask_account

masked = get_mask_account("73654108430135874305")
print(masked)  # **4305

### Модуль widget
Содержит функции для работы с виджетом банковских операций.

mask_account_card(account_card_info: str) -> str
Принимает строку с типом и номером карты или счета, возвращает строку с замаскированным номером.

Пример:
from src.widget import mask_account_card

# Для карты
result = mask_account_card("Visa Platinum 7000792289606361")
print(result)  # Visa Platinum 7000 79** **** 6361

# Для счета
result = mask_account_card("Счет 73654108430135874305")
print(result)  # Счет **4305

get_date(date_string: str) -> str
Преобразует дату из формата "2024-03-11T02:26:18.671407" в формат "ДД.ММ.ГГГГ".

Пример:
from src.widget import get_date

date = get_date("2024-03-11T02:26:18.671407")
print(date)  # 11.03.2024

### Модуль processing
Содержит функции для обработки данных банковских операций.

filter_by_state(operations, state='EXECUTED')
Фильтрует список операций по значению ключа state.

Параметры:
operations (List[Dict[str, Any]]) — список словарей с данными операций
state (str) — значение для фильтрации (по умолчанию 'EXECUTED')
Возвращает: Новый список словарей, где state соответствует указанному значению.
Пример:
from src.processing import filter_by_state

operations = [
    {'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
    {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'},
    {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'}
]

# Фильтрация по умолчанию (EXECUTED)
executed = filter_by_state(operations)
print(executed)
# Вывод: [{'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'}, {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'}]

# Фильтрация CANCELED
canceled = filter_by_state(operations, 'CANCELED')
print(canceled)
# Вывод: [{'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'}]

sort_by_date(operations, descending=True)
Сортирует список операций по дате.

Параметры:
operations (List[Dict[str, Any]]) — список словарей с данными операций
descending (bool) — порядок сортировки: True — по убыванию (сначала новые), False — по возрастанию
Возвращает: Новый отсортированный список операций.

Пример:
from src.processing import sort_by_date

operations = [
    {'id': 41428829, 'date': '2019-07-03T18:35:29.512364'},
    {'id': 939719570, 'date': '2018-06-30T02:08:58.425572'},
    {'id': 594226727, 'date': '2018-09-12T21:27:25.241689'},
    {'id': 615064591, 'date': '2018-10-14T08:21:33.419441'}
]

# Сортировка по убыванию (сначала новые)
sorted_desc = sort_by_date(operations)
print(sorted_desc)
# Вывод: сначала операция с датой 2019-07-03, затем 2018-10-14, затем 2018-09-12, затем 2018-06-30

# Сортировка по возрастанию (сначала старые)
sorted_asc = sort_by_date(operations, False)
print(sorted_asc)
# Вывод: сначала операция с датой 2018-06-30, затем 2018-09-12, затем 2018-10-14, затем 2019-07-03

## Разработка

### Установка инструментов разработки
poetry install --with lint

## Проверка кода

# Проверка типов
mypy src/

# Проверка стиля
flake8 src/

# Форматирование
black src/
isort src/

## Лицензия
Этот проект лицензирован по [лицензии MIT](LICENSE).