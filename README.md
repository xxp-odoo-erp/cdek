# CDEK Python SDK v2

Python библиотека для работы с API СДЭК версии 2.0

## Установка

```bash
pip install cdek-sdk-2
```

## Быстрый старт

### Создание клиента

```python
from cdek import CdekClient

# Создание клиента для тестовой среды
client = CdekClient('TEST')

# Создание клиента для production
client = CdekClient('PROD', account='your_account', secure='your_password')
```

### Получение списка городов

```python
# Получить список городов с фильтрацией
cities = client.get_cities({'size': 10, 'city': 'Москва'})

for city in cities:
    print(f"{city.get('city')} - {city.get('code')}")
```

### Расчёт тарифа

```python
from cdek.entity.requests.tariff import Tariff

# Создание объекта для расчёта тарифа
tariff = Tariff()
tariff.set_type(1)  # Тип доставки (1 - курьерская доставка)
tariff.set_tariff_code(136)  # Код тарифа
tariff.set_city_codes(44, 137)  # Коды городов отправителя и получателя
tariff.set_package_weight(1000)  # Вес в граммах

# Расчёт тарифа
result = client.calculate_tariff(tariff)
print(f"Стоимость: {result.get_total_sum()}")
print(f"Срок доставки: {result.get_delivery_period()}")
```

### Создание заказа

```python
from cdek.entity.requests.order import Order
from cdek.entity.requests.location import Location
from cdek.entity.requests.contact import Contact
from cdek.entity.requests.package import Package
from cdek.entity.requests.item import Item
from cdek.entity.requests.money import Money
from cdek.entity.requests.phone import Phone

# Создание заказа
order = Order()

# Номер заказа в системе магазина
order.set_im_number('ORDER-12345')

# Отправитель
sender_location = Location()
sender_location.set_code(44)  # Код города Москвы
order.set_sender_location(sender_location)

sender_contact = Contact()
sender_contact.set_name('Иван Иванов')
sender_phone = Phone()
sender_phone.set_number('+79000000000')
sender_contact.set_phone(sender_phone)
order.set_sender(sender_contact)

# Получатель
recipient_location = Location()
recipient_location.set_code(137)  # Код города Санкт-Петербурга
order.set_recipient_location(recipient_location)

recipient_contact = Contact()
recipient_contact.set_name('Петр Петров')
recipient_phone = Phone()
recipient_phone.set_number('+79111111111')
recipient_contact.set_phone(recipient_phone)
order.set_recipient(recipient_contact)

# Упаковка
package = Package()
package.set_number('1')
package.set_weight(1000)  # Вес в граммах
package.set_length(10)  # Длина в см
package.set_width(10)  # Ширина в см
package.set_height(10)  # Высота в см

# Товар
item = Item()
item.set_name('Товар тест')
item.set_ware_key('12345')
item.set_amount(1)
item.set_cost(1000)  # Стоимость в рублях

money = Money()
money.set_sum(1000)
money.set_sum_nds(200)
item.set_payment(money)

package.set_items([item])
order.set_packages([package])

# Отдельные параметры заказа
order.set_type(1)  # Тип доставки
order.set_tariff_code(136)  # Код тарифа

# Создание заказа
result = client.create_order(order)
print(f"Заказ создан: {result.get_entity().get_uuid()}")
```

### Получение информации о заказе

```python
# По трек-номеру
order_info = client.get_order_info_by_cdek_number('GRZ123456')

# По номеру заказа в системе магазина
order_info = client.get_order_info_by_im_number('ORDER-12345')

# По UUID заказа
order_info = client.get_order_info_by_uuid('order-uuid')
```

### Получение PDF документов

```python
# Получение ШК-места
barcode_pdf = client.get_barcode_pdf('barcode-uuid')
with open('barcode.pdf', 'wb') as f:
    f.write(barcode_pdf)

# Получение накладной
invoice_pdf = client.get_invoice_pdf('invoice-uuid')
with open('invoice.pdf', 'wb') as f:
    f.write(invoice_pdf)
```

## Основные возможности

- ✅ Автоматическая авторизация с кэшированием токена
- ✅ Получение справочников (регионы, города, ПВЗ)
- ✅ Расчёт стоимости доставки
- ✅ Создание и управление заказами
- ✅ Получение информации о заказах
- ✅ Работа с накладными и ШК
- ✅ Создание договоренностей для курьера
- ✅ Заявки на вызов курьера
- ✅ Управление webhook'ами
- ✅ Получение реестров и платежей
- ✅ Получение чеков
- ✅ Полная поддержка API СДЭК v2

## Обработка ошибок

```python
from cdek.exceptions import CdekException, CdekAuthException, CdekRequestException

try:
    result = client.get_cities({'size': 10})
except CdekAuthException as e:
    print(f"Ошибка авторизации: {e}")
except CdekRequestException as e:
    print(f"Ошибка запроса: {e}")
    print(f"Код статуса: {e.status_code}")
except CdekException as e:
    print(f"Общая ошибка: {e}")
```

## Сохранение токена авторизации

Для уменьшения количества запросов на авторизацию можно сохранять токен:

```python
def save_token(data):
    # Сохранение токена (в базу данных, файл и т.д.)
    with open('token.json', 'w') as f:
        import json
        json.dump(data, f)

def load_token():
    # Загрузка токена
    try:
        with open('token.json', 'r') as f:
            import json
            return json.load(f)
    except FileNotFoundError:
        return None

# Загрузка сохранённого токена
token_data = load_token()
if token_data:
    client.set_memory(token_data['cdekAuth'], save_token)

# Создание клиента
client = CdekClient('PROD', account='your_account', secure='your_password')
```

## Документация

Полная документация по API СДЭК доступна на [https://api.cdek.ru/](https://api.cdek.ru/)

## Лицензия

MIT License

## Поддержка

Если у вас возникли вопросы или проблемы, создайте issue в [GitHub репозитории](https://github.com/cdek/sdk-python)

