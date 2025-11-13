# CDEK Python SDK v2

SDK упрощает работу с API СДЭК версии 2.0: авторизация, справочники, расчёт тарифов, создание заказов, печатные формы, вебхуки и прочие операции доступны через единый клиент.

## Установка

```bash
pip install cdek
```

## Быстрый старт

### Создание клиента

```python
from cdek.client import CdekClient

# Тестовый клиент (использует демо-учётные данные)
test_client = CdekClient("TEST")

# Боевой клиент
prod_client = CdekClient(account="YOUR_ACCOUNT", secure="YOUR_SECURE_PASSWORD")
```

### Получение справочника городов

```python
from cdek.apps.location.filters import CityListFilter

filters = CityListFilter(city="Москва", size=5)
cities = test_client.location.cities(filters)

for city in cities:
    print(f"{city.city} — код {city.code}")
```

### Расчёт тарифа по коду

```python
from cdek.apps.tariff.requests import TariffCodeRequest

request = TariffCodeRequest.init(tariff_code=136)
request.set_city_codes(from_location=44, to_location=137)
request.set_package_weight(weight=1_000)

tariff = test_client.tariff.calc(request)
print(f"Стоимость: {tariff.delivery_sum} {tariff.currency}")
print(f"Срок доставки: {tariff.period_min}–{tariff.period_max} дней")
```

### Создание заказа

```python
from cdek.apps.order.requests import OrderRequest

order = OrderRequest.init(
    number="ORDER-12345",
    tariff_code=136,
)

order.set_from_location(order.location_init(code=44))
order.set_to_location(order.location_init(code=137))

sender = order.contact_init(name="Иван Иванов")
sender.add_phone("+79000000000")
order.set_contact(sender)

recipient = order.contact_init(name="Пётр Петров")
recipient.add_phone("+79111111111")
order.set_recipient(recipient)

package = order.package_init(number="1", weight=1_000)
order.add_package(package)

response = test_client.order.create(order)
print(f"UUID заказа: {response.get_entry_uuid()}")
```

### Получение PDF-документов

```python
barcode_bytes = test_client.barcode.get_pdf("barcode-uuid")
with open("barcode.pdf", "wb") as file:
    file.write(barcode_bytes)

invoice_bytes = test_client.invoice.get_pdf("invoice-uuid")
with open("invoice.pdf", "wb") as file:
    file.write(invoice_bytes)
```

## Обработка ошибок

```python
from cdek.exceptions import CdekAuthException, CdekRequestException

try:
    cities = test_client.location.cities(CityListFilter(size=10))
except CdekAuthException as error:
    print(f"Ошибка авторизации: {error}")
except CdekRequestException as error:
    print(f"Ошибка запроса: {error} (HTTP {error.status_code})")
```

## Сохранение токена авторизации

```python
import json
from pathlib import Path

TOKEN_PATH = Path("token.json")

def save_token(data):
    TOKEN_PATH.write_text(json.dumps(data), encoding="utf-8")

def load_token():
    if TOKEN_PATH.exists():
        return json.loads(TOKEN_PATH.read_text(encoding="utf-8"))
    return None

client = CdekClient(account="YOUR_ACCOUNT", secure="YOUR_SECURE_PASSWORD")
memory = load_token()
if memory:
    client.set_memory(memory.get("cdekAuth"), save_token)
else:
    client.set_memory(None, save_token)
```

## Полезные ссылки

- Официальная документация API: <https://apidoc.cdek.ru>
- Поддержка и вопросы: создавайте issue в репозитории <https://github.com/cdek/sdk-python>

## Лицензия

MIT License
