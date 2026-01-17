(examples)=

# Примеры использования

В этом разделе представлены практические примеры использования CDEK Python SDK для различных сценариев.

## Создание и управление заказами

### Создание заказа с несколькими упаковками

```python
from cdek import CdekClient
from cdek.apps.order.requests import OrderRequest
from cdek.apps.models.location import OrderLocation
from cdek.apps.models.contact import Contact
from cdek.apps.models.package import Package
from cdek.apps.models.item import Item

client = CdekClient("TEST")

order = OrderRequest(
    number="MULTI-PACK-001",
    tariff_code=139,
    from_location=OrderLocation(code=270, address="Склад, ул. Складская, 1"),
    to_location=OrderLocation(code=137, address="Офис, Невский пр., 28"),
    sender=Contact(
        name="ООО Магазин",
        company="ООО Магазин",
        email="sender@example.com",
        phones=[{"number": "+79991234567"}]
    ),
    recipient=Contact(
        name="Иван Иванов",
        email="recipient@example.com",
        phones=[{"number": "+79997654321"}]
    ),
    packages=[
        Package(
            number="PACK-001",
            weight=1500,
            length=20,
            width=15,
            height=10,
            items=[
                Item(name="Товар 1", ware_key="SKU-001", cost=500, amount=1)
            ]
        ),
        Package(
            number="PACK-002",
            weight=2500,
            length=30,
            width=20,
            height=15,
            items=[
                Item(name="Товар 2", ware_key="SKU-002", cost=1000, amount=2)
            ]
        )
    ]
)

response = client.order.create(order)
print(f"Заказ создан: {response.entity.uuid}")
```

### Создание заказа с дополнительными услугами

```python
from cdek.apps.models.order import AdditionalService

order = OrderRequest(
    number="SERVICE-ORDER-001",
    tariff_code=139,
    from_location=OrderLocation(code=270, address="ул. Ленина, д. 1"),
    to_location=OrderLocation(code=137, address="Невский проспект, д. 28"),
    sender=Contact(name="Отправитель", phones=[{"number": "+79991234567"}]),
    recipient=Contact(name="Получатель", phones=[{"number": "+79997654321"}]),
    packages=[
        Package(
            number="PACK-001",
            weight=2000,
            items=[
                Item(name="Товар", ware_key="SKU-001", cost=1000, amount=1)
            ]
        )
    ],
    services=[
        AdditionalService(code="INSURANCE"),  # Страхование
        AdditionalService(code="SMS"),  # SMS уведомление
        AdditionalService(code="CALL")  # Прозвон получателя
    ]
)

response = client.order.create(order)
```

### Отслеживание статуса заказа

```python
import time

# Создание заказа
order_response = client.order.create(order)
order_uuid = order_response.entity.uuid

# Периодическая проверка статуса
while True:
    order_info = client.order.get_by_uuid(order_uuid)
    status = order_info.entity.statuses[0].name if order_info.entity.statuses else "Неизвестно"
    print(f"Статус заказа: {status}")

    if status == "Вручен":
        print("Заказ доставлен!")
        break

    time.sleep(60)  # Проверка каждую минуту
```

## Работа с тарифами

### Сравнение тарифов

```python
from cdek.apps.tariff.requests import TariffListRequest

tariff_request = TariffListRequest()
tariff_request.set_city_codes(from_location=270, to_location=137)
tariff_request.set_package_weight(5000)  # 5 кг

tariffs = client.tariff.calc_list(tariff_request)

# Сортировка по стоимости
sorted_tariffs = sorted(
    tariffs.tariff_codes,
    key=lambda x: x.delivery_sum
)

print("Тарифы отсортированные по стоимости:")
for tariff in sorted_tariffs:
    print(f"Тариф {tariff.tariff_code}: {tariff.delivery_sum} руб., "
          f"срок: {tariff.delivery_period} дней")
```

### Расчет с учетом дополнительных услуг

```python
from cdek.apps.tariff.requests import TariffCodeRequest, CalcAdditionalService, CalculatorLocation

tariff_request = TariffCodeRequest(
    tariff_code=139,
    from_location=CalculatorLocation(code=270),
    to_location=CalculatorLocation(code=137),
    packages=[CalcPackage(weight=2000)],
    services=[
        CalcAdditionalService(code="INSURANCE", parameter="1000")
    ]
)

result = client.tariff.calc(tariff_request)
print(f"Общая стоимость: {result.total_sum} руб.")
print(f"Стоимость доставки: {result.delivery_sum} руб.")
print(f"Стоимость услуг: {result.services_sum} руб.")
```

## Работа с локациями

### Поиск города с автодополнением

```python
from cdek.apps.location.filters import CityFilter

# Поиск города
city = client.location.city(CityFilter(city="Мос"))

if city:
    print(f"Найден: {city.city} (код: {city.code})")
    print(f"Регион: {city.region}")
    print(f"Страна: {city.country}")
```

### Получение всех городов в регионе

```python
from cdek.apps.location.filters import CityListFilter

# Получение всех городов Московской области
cities = client.location.cities(CityListFilter(region_code=77))

print(f"Найдено городов: {len(cities)}")
for city in cities[:10]:  # Первые 10
    print(f"- {city.city} (код: {city.code})")
```

### Определение локации по адресу через координаты

```python
from cdek.apps.location.filters import CoordinatesFilter

# Координаты Красной площади в Москве
locations = client.location.coordinates(
    CoordinatesFilter(latitude=55.7558, longitude=37.6173)
)

if locations:
    location = locations[0]
    print(f"Город: {location.city}")
    print(f"Код города: {location.code}")
    print(f"Адрес: {location.address}")
```

## Работа с ПВЗ

### Поиск ближайших ПВЗ

```python
from cdek.apps.office.filters import OfficeFilter

# Поиск ПВЗ в городе с фильтрацией
filter_params = OfficeFilter(
    city_code=270,
    type="PVZ"  # Только пункты выдачи
)

offices = client.office.get(filter_params)

print(f"Найдено ПВЗ: {len(offices['result'])}")
for office in offices["result"][:5]:  # Первые 5
    print(f"\n{office.name}")
    print(f"Адрес: {office.address}")
    print(f"Режим работы: {office.work_time}")
    if office.location:
        print(f"Координаты: {office.location.latitude}, {office.location.longitude}")
```

## Работа с вебхуками

### Настройка вебхуков для отслеживания заказов

```python
from cdek.apps.webhook.requests import WebhookRequest
from cdek.apps.webhook.enums import WebhookType

# Создание вебхука для отслеживания статусов заказов
webhook = WebhookRequest(
    url="https://example.com/webhook/order-status",
    type=WebhookType.ORDER_STATUS
)

response = client.webhook.set(webhook)
print(f"Вебхук создан: {response.entity.uuid}")

# Создание вебхука для отслеживания печатных форм
webhook_print = WebhookRequest(
    url="https://example.com/webhook/print-form",
    type=WebhookType.PRINT_FORM
)

response_print = client.webhook.set(webhook_print)
print(f"Вебхук для печатных форм создан: {response_print.entity.uuid}")
```

### Получение и управление вебхуками

```python
# Получение всех вебхуков
webhooks = client.webhook.all()

print("Активные вебхуки:")
for webhook in webhooks:
    print(f"- {webhook.type}: {webhook.url} (UUID: {webhook.uuid})")

# Удаление вебхука
if webhooks:
    client.webhook.delete(webhooks[0].uuid)
    print("Вебхук удален")
```

## Обработка ошибок

### Обработка различных типов ошибок

```python
from cdek.exceptions import (
    CdekAuthException,
    CdekRequestException,
    CdekException
)

try:
    # Попытка создать заказ с неверными данными
    order = OrderRequest(
        number="INVALID-ORDER",
        tariff_code=999,  # Несуществующий тариф
        # ... остальные параметры
    )
    response = client.order.create(order)

except CdekAuthException as e:
    print(f"Ошибка авторизации: {e}")
    print("Проверьте учетные данные")

except CdekRequestException as e:
    print(f"Ошибка запроса: {e}")
    print(f"Код ответа: {e.status_code}")
    if e.response:
        print(f"Детали ошибки: {e.response}")

except CdekException as e:
    print(f"Общая ошибка CDEK: {e}")

except Exception as e:
    print(f"Неожиданная ошибка: {e}")
```

### Повторные попытки при ошибках

```python
import time
from cdek.exceptions import CdekRequestException

def create_order_with_retry(order, max_retries=3):
    """Создание заказа с повторными попытками"""
    for attempt in range(max_retries):
        try:
            return client.order.create(order)
        except CdekRequestException as e:
            if attempt < max_retries - 1:
                wait_time = 2 ** attempt  # Экспоненциальная задержка
                print(f"Ошибка, повтор через {wait_time} сек...")
                time.sleep(wait_time)
            else:
                raise

# Использование
try:
    response = create_order_with_retry(order)
    print(f"Заказ создан: {response.entity.uuid}")
except CdekRequestException as e:
    print(f"Не удалось создать заказ после {max_retries} попыток: {e}")
```

## Сохранение и использование токена

### Кэширование токена в файл

```python
import json
import os

TOKEN_FILE = "cdek_token.json"

def load_token():
    """Загрузка токена из файла"""
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, "r") as f:
            return json.load(f)
    return {}

def save_token(data):
    """Сохранение токена в файл"""
    with open(TOKEN_FILE, "w") as f:
        json.dump(data, f)

# Загрузка сохраненного токена
memory = load_token()

# Создание клиента с сохранением токена
client = CdekClient("TEST")
client.set_memory(memory, save_token)

# Теперь токен будет автоматически сохраняться и использоваться
order_info = client.order.get_by_uuid("some-uuid")
```

## Интеграция с базой данных

### Сохранение заказа в базу данных

```python
# Пример с использованием SQLAlchemy (псевдокод)
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Создание заказа через API
order_response = client.order.create(order)

# Сохранение в БД
db_order = DBOder(
    cdek_uuid=order_response.entity.uuid,
    cdek_number=order_response.entity.cdek_number,
    im_number=order.number,
    status="CREATED"
)
session.add(db_order)
session.commit()
```

## Пакетная обработка заказов

### Создание нескольких заказов

```python
orders_data = [
    {"number": "ORDER-001", "recipient": "Иван Иванов", ...},
    {"number": "ORDER-002", "recipient": "Петр Петров", ...},
    {"number": "ORDER-003", "recipient": "Сидор Сидоров", ...},
]

created_orders = []
failed_orders = []

for order_data in orders_data:
    try:
        order = OrderRequest(**order_data)
        response = client.order.create(order)
        created_orders.append({
            "im_number": order_data["number"],
            "cdek_uuid": response.entity.uuid
        })
    except Exception as e:
        failed_orders.append({
            "im_number": order_data["number"],
            "error": str(e)
        })

print(f"Создано заказов: {len(created_orders)}")
print(f"Ошибок: {len(failed_orders)}")
```
