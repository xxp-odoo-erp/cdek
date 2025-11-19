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

## Документация API

### Клиент (CdekClient)

#### Конструктор

```python
CdekClient(account: str, secure: str | None = None, timeout: float = 5.0)
```

**Параметры:**
- `account` (str): Логин Account в сервисе Интеграции. Для тестового режима используйте `"TEST"`
- `secure` (str | None): Пароль Secure password в сервисе Интеграции. Не требуется для тестового режима
- `timeout` (float): Тайм-аут запроса в секундах (по умолчанию 5.0)

#### Методы клиента

##### `set_memory(memory: dict | None, save_callback: Callable) -> CdekClient`

Установить параметры сохранения токена авторизации.

**Параметры:**
- `memory` (dict | None): Словарь с сохранёнными данными авторизации
- `save_callback` (Callable): Функция для сохранения токена

**Возвращает:** `CdekClient` (self)

---

### Тарифы (client.tariff)

#### `calc(tariff: TariffCodeRequest) -> TariffResponse`

Расчёт стоимости и сроков доставки по коду тарифа.

**Параметры:**
- `tariff` (TariffCodeRequest): Объект с параметрами запроса:
  - `tariff_code` (int): Код тарифа
  - `from_location` (CalculatorLocation): Адрес отправления
  - `to_location` (CalculatorLocation): Адрес получения
  - `packages` (list[CalcPackage]): Список упаковок
  - `services` (list[CalcAdditionalService] | None): Список дополнительных услуг
  - `date` (datetime | None): Дата и время планируемой передачи заказа
  - `type` (int): Тип заказа (1 — интернет-магазин, 2 — доставка)
  - `currency` (int | None): Валюта расчёта
  - `lang` (str): Язык вывода информации (rus, eng, zho)

**Возвращает:** `TariffResponse` — объект с информацией о стоимости и сроках доставки

#### `calc_list(tariff: TariffListRequest) -> TariffListResponse`

Расчёт стоимости и сроков доставки по всем доступным тарифам.

**Параметры:**
- `tariff` (TariffListRequest): Объект с параметрами запроса (аналогично `calc`, но без `tariff_code`)

**Возвращает:** `TariffListResponse` — список доступных тарифов

#### `all() -> TariffAvailableResponse`

Получить список всех доступных тарифов по договору.

**Возвращает:** `TariffAvailableResponse` — список доступных тарифов

---

### Заказы (client.order)

#### `create(order: OrderRequest) -> EntityResponse`

Создать заказ в системе CDEK.

**Параметры:**
- `order` (OrderRequest): Объект с информацией о заказе:
  - `number` (str): Номер заказа в системе отправителя
  - `tariff_code` (int): Код тарифа
  - `from_location` (Location): Адрес отправления
  - `to_location` (Location): Адрес получения
  - `recipient` (Contact): Контакт получателя
  - `sender` (Contact): Контакт отправителя
  - `packages` (list[Package]): Список упаковок
  - `print` (str | None): Тип печатной формы
  - `widget_token` (str | None): Токен CMS

**Возвращает:** `EntityResponse` — объект с информацией о созданном заказе

#### `update(order: OrderUpdateRequest) -> EntityResponse`

Обновить сведения по ранее созданному заказу.

**Параметры:**
- `order` (OrderUpdateRequest): Объект с информацией об обновлении заказа:
  - `uuid` (str | None): Идентификатор заказа в ИС СДЭК
  - `cdek_number` (int | None): Номер заказа в ИС СДЭК
  - Остальные поля аналогичны `OrderRequest`

**Возвращает:** `EntityResponse` — объект с информацией об обновлённом заказе

#### `delete(uuid: str) -> EntityResponse`

Удалить заказ по его UUID.

**Параметры:**
- `uuid` (str): Идентификатор заказа

**Возвращает:** `EntityResponse` — объект с информацией об удалённом заказе

#### `get_by_uuid(uuid: str) -> OrderEntityResponse`

Получить полную информацию о заказе по UUID.

**Параметры:**
- `uuid` (str): Идентификатор заказа

**Возвращает:** `OrderEntityResponse` — объект с информацией о заказе

#### `get_by_cdek_number(cdek_number: str) -> OrderEntityResponse`

Получить полную информацию о заказе по трек-номеру.

**Параметры:**
- `cdek_number` (str): Трек-номер заказа

**Возвращает:** `OrderEntityResponse` — объект с информацией о заказе

#### `get_by_im_number(im_number: str) -> OrderEntityResponse`

Получить полную информацию о заказе по ID заказа в магазине.

**Параметры:**
- `im_number` (str): ID заказа в магазине

**Возвращает:** `OrderEntityResponse` — объект с информацией о заказе

#### `client_return(uuid: str, tariff_code: int) -> EntityResponse`

Зарегистрировать клиентский возврат.

**Параметры:**
- `uuid` (str): Идентификатор заказа
- `tariff_code` (int): Код тарифа

**Возвращает:** `EntityResponse` — объект с информацией о регистрации возврата

---

### Локации (client.location)

#### `cities(filter_params: CityListFilter | None = None) -> list[CitiesResponse]`

Получить список населённых пунктов.

**Параметры:**
- `filter_params` (CityListFilter | None): Фильтр для поиска:
  - `city` (str | None): Название населённого пункта
  - `code` (int | None): Код населённого пункта СДЭК
  - `country_codes` (str | None): Коды стран в формате ISO_3166-1_alpha-2
  - `region_code` (int | None): Код региона
  - `postal_code` (str | None): Почтовый индекс
  - `size` (int | None): Ограничение выборки (по умолчанию 1000)
  - `page` (int | None): Номер страницы (нумерация с 0)
  - `lang` (str | None): Язык локализации

**Возвращает:** `list[CitiesResponse]` — список городов

#### `city(filter_params: CityFilter) -> CityResponse | None`

Подобрать локацию по названию города.

**Параметры:**
- `filter_params` (CityFilter): Фильтр для подбора:
  - `name` (str): Наименование населённого пункта
  - `country_code` (str | None): Код страны в формате ISO_3166-1_alpha-2

**Возвращает:** `CityResponse | None` — информация о найденном городе или None

#### `regions(filter_params: RegionFilter | None = None) -> list[RegionResponse]`

Получить список регионов.

**Параметры:**
- `filter_params` (RegionFilter | None): Фильтр для поиска:
  - `country_codes` (str | None): Список кодов стран
  - `size` (int): Ограничение выборки (по умолчанию 1000)
  - `page` (int): Номер страницы (по умолчанию 0)
  - `lang` (Literal["rus", "zho"]): Локализация (по умолчанию "rus")

**Возвращает:** `list[RegionResponse]` — список регионов

#### `zip(filter_params: ZipFilter | None = None) -> list[ZipResponse]`

Получить почтовые индексы города.

**Параметры:**
- `filter_params` (ZipFilter | None): Фильтр для поиска:
  - `city_code` (int): Код города

**Возвращает:** `list[ZipResponse]` — список почтовых индексов

#### `coordinates(filter_params: CoordinatesFilter | None = None) -> list[CoordinatesResponse]`

Получить локацию по координатам.

**Параметры:**
- `filter_params` (CoordinatesFilter | None): Фильтр для поиска:
  - `latitude` (float): Широта
  - `longitude` (float): Долгота

**Возвращает:** `list[CoordinatesResponse]` — список локаций

---

### ПВЗ (client.office)

#### `get(filter_params: OfficeFilter | None = None) -> list[OfficeResponse]`

Получить список пунктов выдачи заказов (ПВЗ) СДЭК.

**Параметры:**
- `filter_params` (OfficeFilter | None): Фильтр для поиска:
  - `code` (str | None): Код ПВЗ
  - `type` (Literal["PVZ", "POSTAMAT", "ALL"]): Тип офиса (по умолчанию "ALL")
  - `postal_code` (str | None): Почтовый индекс города
  - `city_code` (int | None): Код населённого пункта СДЭК
  - `country_code` (str | None): Код страны в формате ISO_3166-1_alpha-2
  - `region_code` (int | None): Код региона СДЭК
  - `have_cashless` (bool | None): Наличие терминала оплаты
  - `have_cash` (bool | None): Есть приём наличных
  - `is_dressing_room` (bool | None): Наличие примерочной
  - `weight_max` (int | None): Максимальный вес в кг
  - `weight_min` (int | None): Минимальный вес в кг
  - `lang` (str): Локализация (по умолчанию "rus")
  - `take_only` (bool | None): Только пункт выдачи
  - `size` (int | None): Ограничение выборки
  - `page` (int | None): Номер страницы

**Возвращает:** `list[OfficeResponse]` — список ПВЗ

---

### Штрих-коды (client.barcode)

#### `set(barcode: PrintBarcodeRequest) -> EntityResponse`

Запросить формирование штрих-кода к заказу.

**Параметры:**
- `barcode` (PrintBarcodeRequest): Объект с информацией о запросе:
  - `order_uuid` (str): UUID заказа
  - `format` (Literal["A4", "A5", "A6", "A7"]): Формат печати (по умолчанию "A4")
  - `lang` (Literal["RUS", "ENG"]): Язык печати (по умолчанию "RUS")

**Возвращает:** `EntityResponse` — объект с информацией о формировании штрих-кода

#### `get(uuid: str) -> PrintBarcodeResponse`

Получить сущность штрих-кода к заказу.

**Параметры:**
- `uuid` (str): Идентификатор штрих-кода

**Возвращает:** `PrintBarcodeResponse` — объект с информацией о штрих-коде

#### `get_pdf(uuid: str) -> bytes`

Скачать готовый штрих-код в формате PDF.

**Параметры:**
- `uuid` (str): Идентификатор штрих-кода

**Возвращает:** `bytes` — содержимое PDF файла

---

### Накладные (client.invoice)

#### `set(invoice: PrintInvoiceRequest) -> EntityResponse`

Запросить формирование накладной к заказу.

**Параметры:**
- `invoice` (PrintInvoiceRequest): Объект с информацией о запросе:
  - `order_uuid` (str): UUID заказа
  - `type` (PrintType | None): Тип накладной

**Возвращает:** `EntityResponse` — объект с информацией о формировании накладной

#### `get(uuid: str) -> WaybillEntityResponse`

Получить сущность накладной к заказу.

**Параметры:**
- `uuid` (str): Идентификатор накладной (UUID заказа)

**Возвращает:** `WaybillEntityResponse` — объект с информацией о накладной

#### `get_pdf(uuid: str) -> bytes`

Получить PDF накладной к заказу.

**Параметры:**
- `uuid` (str): Идентификатор накладной (UUID заказа)

**Возвращает:** `bytes` — содержимое PDF файла

---

### Платежи (client.payment)

#### `get(date: Date) -> PaymentInfoResponse`

Получить информацию о переводе наложенного платежа.

**Параметры:**
- `date` (Date): Дата для получения информации о переводе

**Возвращает:** `PaymentInfoResponse` — объект с информацией о переводе

#### `get_registries(date: Date) -> PaymentResponse`

Получить информацию о реестрах наложенного платежа.

**Параметры:**
- `date` (Date): Дата для получения информации о реестрах

**Возвращает:** `PaymentResponse` — объект с информацией о реестрах

---

### Договорённости о доставке (client.agreement)

#### `create(agreement: RegisterDeliveryRequest) -> EntityResponse`

Зарегистрировать договорённость о доставке.

**Параметры:**
- `agreement` (RegisterDeliveryRequest): Объект с информацией о договорённости:
  - `order_uuid` (str): UUID заказа
  - `date` (Date): Дата доставки, согласованная с получателем
  - `time_from` (str): Время доставки "С"
  - `time_to` (str): Время доставки "По"
  - `comment` (str | None): Комментарий
  - `delivery_point` (str | None): Буквенно-цифровой код ПВЗ СДЭК
  - `to_location` (ScheduleLocation | None): Населённый пункт

**Возвращает:** `EntityResponse` — объект с информацией о регистрации

#### `get(uuid: str) -> AgreementInfoResponse`

Получить договорённости для курьера.

**Параметры:**
- `uuid` (str): UUID договора

**Возвращает:** `AgreementInfoResponse` — объект с информацией о договоре

#### `get_interval_number(cdek_number: str) -> AvailableDeliveryIntervalsResponse`

Получить интервалы доставки по номеру заказа.

**Параметры:**
- `cdek_number` (str): Номер заказа

**Возвращает:** `AvailableDeliveryIntervalsResponse` — объект с интервалами доставки

#### `get_interval_uuid(uuid: str) -> AvailableDeliveryIntervalsResponse`

Получить интервалы доставки по UUID заказа.

**Параметры:**
- `uuid` (str): UUID заказа

**Возвращает:** `AvailableDeliveryIntervalsResponse` — объект с интервалами доставки

#### `get_intervals_before_create_order(request: DeliveryIntervalRequest) -> AvailableDeliveryIntervalsResponse`

Получить интервалы доставки до создания заказа.

**Параметры:**
- `request` (DeliveryIntervalRequest): Объект с информацией о запросе:
  - `date_time` (datetime): Дата и время заявки на вызов курьера
  - `from_location` (DeliveryLocation | None): Адрес отправления
  - `shipment_point` (str | None): Код ПВЗ СДЭК
  - `to_location` (DeliveryLocation): Адрес доставки
  - `tariff_code` (int): Код тарифа
  - `additional_order_types` (list[int] | None): Дополнительные типы заказа

**Возвращает:** `AvailableDeliveryIntervalsResponse` — объект с интервалами доставки

---

### Заявки на вызов курьера (client.intake)

#### `create(intake: IntakeRequest) -> EntityResponse`

Создать заявку на вызов курьера.

**Параметры:**
- `intake` (IntakeRequest): Объект с информацией о заявке:
  - `intake_date` (Date): Дата забора
  - `intake_time_from` (str): Время начала забора
  - `intake_time_to` (str): Время окончания забора
  - `lunch_time_from` (str | None): Время начала обеда
  - `lunch_time_to` (str | None): Время окончания обеда
  - `from_location` (IntakeLocation): Адрес отправления
  - `sender` (Contact): Контакт отправителя
  - `comment` (str | None): Комментарий

**Возвращает:** `EntityResponse` — объект с информацией о созданной заявке

#### `get(uuid: str) -> IntakeEntityResponse`

Получить информацию о заявке на вызов курьера.

**Параметры:**
- `uuid` (str): Идентификатор заявки

**Возвращает:** `IntakeEntityResponse` — объект с информацией о заявке

#### `update(intake: IntakeFilter) -> EntityResponse`

Изменить параметры существующей заявки.

**Параметры:**
- `intake` (IntakeFilter): Объект с информацией об изменении:
  - `uuid` (UUID): Идентификатор заявки
  - `status` (IntakeStatus): Статус заявки:
    - `code` (str): Код статуса
    - `add_status` (str): Дополнительный код статуса

**Возвращает:** `EntityResponse` — объект с информацией об изменённой заявке

#### `delete(uuid: str) -> EntityResponse`

Удалить заявку на вызов курьера.

**Параметры:**
- `uuid` (str): Идентификатор заявки

**Возвращает:** `EntityResponse` — объект с информацией об удалённой заявке

#### `get_call_dates(date_request: IntakeDateFilter) -> IntakeDateResponse`

Получить доступные даты вызова курьера.

**Параметры:**
- `date_request` (IntakeDateFilter): Фильтр для получения дат:
  - `from_location` (IntakeLocation): Адрес отправления
  - `date` (Date): До какого числа включительно получить доступные дни

**Возвращает:** `IntakeDateResponse` — объект с доступными датами

---

### Чеки (client.check)

#### `get(filter_params: CheckFilter) -> CheckResponse`

Получить информацию о чеке по заказу или за выбранный день.

**Параметры:**
- `filter_params` (CheckFilter): Фильтр для получения информации:
  - `order_uuid` (str | None): Идентификатор заказа
  - `cdek_number` (str | None): Номер заказа СДЭК
  - `date` (Date | None): Дата создания чека в формате YYYY-MM-DD

**Возвращает:** `CheckResponse` — объект с информацией о чеке

---

### Вебхуки (client.webhook)

#### `all() -> list[WebhookResponse]`

Получить информацию о всех слушателях webhook.

**Возвращает:** `list[WebhookResponse]` — список слушателей webhook

#### `get(uuid: str) -> WebhookUUIDEntityResponse`

Получить информацию о слушателе webhook.

**Параметры:**
- `uuid` (str): Идентификатор слушателя webhook

**Возвращает:** `WebhookUUIDEntityResponse` — объект с информацией о слушателе

#### `set(webhook: WebhookRequest) -> WebookSetEntityResponse`

Добавить нового слушателя webhook.

**Параметры:**
- `webhook` (WebhookRequest): Объект с информацией о webhook:
  - `type` (WebhookType): Тип вебхука (ORDER_STATUS, ORDER_MODIFIED, PRINT_FORM, RECEIPT, DOWNLOAD_PHOTO, PREALERT_CLOSED, ACCOMPANYING_WAYBILL, OFFICE_AVAILABILITY, DELIV_PROBLEM, DELIV_AGREEMENT)
  - `url` (str): URL, на который отправляется событие

**Возвращает:** `WebookSetEntityResponse` — объект с информацией о добавленном слушателе

#### `delete(uuid: str) -> WebhookDeleteEntityResponse`

Удалить слушателя webhook.

**Параметры:**
- `uuid` (str): Идентификатор слушателя webhook

**Возвращает:** `WebhookDeleteEntityResponse` — объект с информацией об удалённом слушателе

---

### Валюта (client.currency)

#### `get(currency_code: str) -> int`

Получить числовой код валюты по её символьному обозначению.

**Параметры:**
- `currency_code` (str): Символьный код валюты (например, "RUB", "USD", "EUR")

**Возвращает:** `int` — числовой код валюты

**Поддерживаемые валюты:** RUB, KZT, USD, EUR, GBP, CNY, BYR, UAH, KGS, AMD, TRY, THB, KRW, AED, UZS, MNT, PLN, AZN, GEL, JPY, VND

#### `all() -> list[int]`

Получить список всех поддерживаемых кодов валют.

**Возвращает:** `list[int]` — список числовых кодов валют

---

## Полезные ссылки

- Официальная документация API: <https://apidoc.cdek.ru>
- Поддержка и вопросы: создавайте issue в репозитории <https://github.com/xxp-odoo-erp/cdek/issues>

## Лицензия

MIT License
