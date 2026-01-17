(usage)=

# Использование

После {ref}`установки <installation>` библиотеки вы можете начать использовать CDEK Python SDK для работы с API СДЭК версии 2.0.

## Быстрый старт

### Создание клиента

Для начала работы создайте экземпляр `CdekClient`:

```python
from cdek import CdekClient

# Использование тестового аккаунта
client = CdekClient("TEST")

# Или использование реального аккаунта
client = CdekClient(
    account="ваш_логин",
    secure="ваш_пароль",
    timeout=10.0  # таймаут запросов в секундах
)
```

### Работа с заказами

#### Создание заказа

```python
from cdek.apps.order.requests import OrderRequest
from cdek.apps.models.location import OrderLocation
from cdek.apps.models.contact import Contact
from cdek.apps.models.package import Package
from cdek.apps.models.item import Item

# Создание запроса на создание заказа
order = OrderRequest(
    number="ORDER-12345",  # Номер заказа в вашей системе
    tariff_code=139,  # Код тарифа
    from_location=OrderLocation(
        code=270,  # Код города отправителя (Москва)
        address="ул. Ленина, д. 1"
    ),
    to_location=OrderLocation(
        code=137,  # Код города получателя (Санкт-Петербург)
        address="Невский проспект, д. 28"
    ),
    sender=Contact(
        name="Иван Иванов",
        phones=[{"number": "+79991234567"}]
    ),
    recipient=Contact(
        name="Петр Петров",
        phones=[{"number": "+79997654321"}]
    ),
    packages=[
        Package(
            number="PACK-001",
            weight=2000,  # Вес в граммах
            items=[
                Item(
                    name="Товар 1",
                    ware_key="SKU-001",
                    cost=1000,  # Стоимость в рублях
                    amount=1
                )
            ]
        )
    ]
)

# Создание заказа
response = client.order.create(order)
print(f"Заказ создан: {response.entity.uuid}")
```

#### Получение информации о заказе

```python
# По UUID
order_info = client.order.get_by_uuid("uuid-заказа")

# По трек-номеру СДЭК
order_info = client.order.get_by_cdek_number("CDEK123456")

# По номеру заказа в вашей системе
order_info = client.order.get_by_im_number("ORDER-12345")
```

#### Обновление заказа

```python
from cdek.apps.order.requests import OrderUpdateRequest

update_request = OrderUpdateRequest(
    uuid="uuid-заказа",
    recipient=Contact(
        name="Новое имя получателя",
        phones=[{"number": "+79999999999"}]
    )
)

response = client.order.update(update_request)
```

#### Удаление заказа

```python
response = client.order.delete("uuid-заказа")
```

### Расчет стоимости доставки

#### Расчет по всем доступным тарифам

```python
from cdek.apps.tariff.requests import TariffListRequest
from cdek.apps.models.package import CalcPackage

tariff_request = TariffListRequest()
tariff_request.set_city_codes(
    from_location=270,  # Москва
    to_location=137     # Санкт-Петербург
)
tariff_request.set_package_weight(2000)  # 2 кг

# Получение списка всех доступных тарифов
tariffs = client.tariff.calc_list(tariff_request)

for tariff in tariffs.tariff_codes:
    print(f"Тариф {tariff.tariff_code}: {tariff.delivery_sum} руб.")
```

#### Расчет по конкретному тарифу

```python
from cdek.apps.tariff.requests import TariffCodeRequest, CalculatorLocation

tariff_request = TariffCodeRequest(
    tariff_code=139,
    from_location=CalculatorLocation(code=270),
    to_location=CalculatorLocation(code=137),
    packages=[CalcPackage(weight=2000)]
)

result = client.tariff.calc(tariff_request)
print(f"Стоимость: {result.total_sum} руб.")
print(f"Срок доставки: {result.delivery_period} дней")
```

#### Получение списка всех доступных тарифов

```python
tariffs = client.tariff.all()
for tariff in tariffs.tariffs:
    print(f"{tariff.tariff_name} (код: {tariff.tariff_code})")
```

### Работа с ПВЗ (пунктами выдачи заказов)

#### Получение списка ПВЗ

```python
from cdek.apps.office.filters import OfficeFilter

# Получение всех ПВЗ в городе
filter_params = OfficeFilter(city_code=270)  # Москва
result = client.office.get(filter_params)

for office in result["result"]:
    print(f"{office.name} - {office.address}")
    print(f"Режим работы: {office.work_time}")
```

### Работа с локациями

#### Поиск города по названию

```python
from cdek.apps.location.filters import CityFilter

city = client.location.city(CityFilter(city="Москва"))
if city:
    print(f"Найден город: {city.city} (код: {city.code})")
```

#### Получение списка регионов

```python
from cdek.apps.location.filters import RegionFilter

regions = client.location.regions()
for region in regions:
    print(f"{region.region} (код: {region.code})")
```

#### Получение списка городов

```python
from cdek.apps.location.filters import CityListFilter

cities = client.location.cities(CityListFilter(region_code=77))  # Московская область
for city in cities:
    print(f"{city.city} (код: {city.code})")
```

#### Определение локации по координатам

```python
from cdek.apps.location.filters import CoordinatesFilter

locations = client.location.coordinates(
    CoordinatesFilter(latitude=55.7558, longitude=37.6173)
)
for location in locations:
    print(f"Город: {location.city}, Код: {location.code}")
```

### Работа с валютами

```python
currencies = client.currency.get()
for currency in currencies:
    print(f"{currency.name}: {currency.code}")
```

### Работа с вебхуками

#### Получение списка вебхуков

```python
webhooks = client.webhook.all()
for webhook in webhooks:
    print(f"URL: {webhook.url}, Тип: {webhook.type}")
```

#### Создание вебхука

```python
from cdek.apps.webhook.requests import WebhookRequest
from cdek.apps.webhook.enums import WebhookType

webhook = WebhookRequest(
    url="https://example.com/webhook",
    type=WebhookType.ORDER_STATUS
)

response = client.webhook.set(webhook)
print(f"Вебхук создан: {response.entity.uuid}")
```

#### Удаление вебхука

```python
response = client.webhook.delete("uuid-вебхука")
```

### Работа с накладными и штрих-кодами

#### Получение накладной

```python
# Получение PDF накладной
pdf_content = client.invoice.get("uuid-заказа", format="pdf")

# Сохранение в файл
with open("invoice.pdf", "wb") as f:
    f.write(pdf_content)
```

#### Получение штрих-кода

```python
# Получение PDF штрих-кода
barcode_content = client.barcode.get("uuid-заказа", format="pdf")

# Сохранение в файл
with open("barcode.pdf", "wb") as f:
    f.write(barcode_content)
```

### Сохранение токена авторизации

Для оптимизации работы с API можно сохранять токен авторизации:

```python
# Словарь для хранения токена
memory = {}

def save_token(data):
    """Коллбэк для сохранения токена"""
    memory.update(data)

# Установка параметров сохранения токена
client.set_memory(memory, save_token)

# При первом запросе токен будет сохранен
# При последующих запросах будет использован сохраненный токен
# до истечения срока его действия
```

## Обработка ошибок

Библиотека предоставляет несколько типов исключений:

```python
from cdek import CdekClient
from cdek.exceptions import (
    CdekException,
    CdekAuthException,
    CdekRequestException
)

try:
    client = CdekClient("TEST")
    order = client.order.get_by_uuid("неверный-uuid")
except CdekAuthException as e:
    print(f"Ошибка авторизации: {e}")
except CdekRequestException as e:
    print(f"Ошибка запроса: {e}")
    print(f"Код ответа: {e.status_code}")
    print(f"Ответ API: {e.response}")
except CdekException as e:
    print(f"Общая ошибка CDEK: {e}")
```

## Дополнительные возможности

### Использование констант

Библиотека предоставляет константы для работы с API:

```python
from cdek import constants

# Коды методов доставки
print(constants.DELIVERY_METHODS)

# Коды услуг
print(constants.SERVICE_CODES)

# Коды ошибок
print(constants.ERRORS)
```

### Настройка таймаута

```python
# Установка таймаута при создании клиента
client = CdekClient("TEST", timeout=30.0)

# Или изменение после создания
client.timeout = 30.0
```
