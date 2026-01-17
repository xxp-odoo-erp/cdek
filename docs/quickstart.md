(quickstart)=

# Быстрый старт

Это руководство поможет вам быстро начать работу с CDEK Python SDK.

## Минимальный пример

Самый простой способ начать работу - использовать тестовый аккаунт:

```python
from cdek import CdekClient

# Создание клиента с тестовым аккаунтом
client = CdekClient("TEST")

# Получение списка доступных тарифов
tariffs = client.tariff.all()
print(f"Доступно тарифов: {len(tariffs.tariffs)}")
```

## Пример создания заказа

```python
from cdek import CdekClient
from cdek.apps.order.requests import OrderRequest
from cdek.apps.models.location import OrderLocation
from cdek.apps.models.contact import Contact
from cdek.apps.models.package import Package
from cdek.apps.models.item import Item

# Создание клиента
client = CdekClient("TEST")

# Создание заказа
order = OrderRequest(
    number="TEST-ORDER-001",
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
    ]
)

# Отправка заказа
response = client.order.create(order)
print(f"Заказ создан: {response.entity.uuid}")
```

## Пример расчета стоимости доставки

```python
from cdek import CdekClient
from cdek.apps.tariff.requests import TariffListRequest

client = CdekClient("TEST")

# Расчет стоимости доставки
tariff_request = TariffListRequest()
tariff_request.set_city_codes(from_location=270, to_location=137)
tariff_request.set_package_weight(2000)

# Получение списка тарифов
tariffs = client.tariff.calc_list(tariff_request)

# Вывод результатов
for tariff in tariffs.tariff_codes:
    print(f"Тариф {tariff.tariff_code}: {tariff.delivery_sum} руб.")
```

## Пример поиска ПВЗ

```python
from cdek import CdekClient
from cdek.apps.office.filters import OfficeFilter

client = CdekClient("TEST")

# Поиск ПВЗ в Москве
offices = client.office.get(OfficeFilter(city_code=270))

for office in offices["result"]:
    print(f"{office.name} - {office.address}")
```

## Следующие шаги

- Изучите {ref}`полное руководство по использованию <usage>`
- Ознакомьтесь с {ref}`API Reference <cdek>` для детальной информации о всех методах
- Посмотрите примеры в разделе {ref}`примеры использования <usage>`
