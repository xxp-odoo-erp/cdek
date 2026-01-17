(errors)=

# Обработка ошибок

CDEK Python SDK предоставляет несколько типов исключений для обработки различных ошибок, которые могут возникнуть при работе с API.

## Типы исключений

### CdekException

Базовый класс для всех исключений CDEK SDK.

```python
from cdek.exceptions import CdekException

try:
    # Ваш код
    pass
except CdekException as e:
    print(f"Ошибка CDEK: {e}")
```

### CdekAuthException

Исключение, возникающее при ошибках авторизации.

```python
from cdek.exceptions import CdekAuthException

try:
    client = CdekClient("неверный_логин", "неверный_пароль")
    # Любой запрос вызовет ошибку авторизации
    client.tariff.all()
except CdekAuthException as e:
    print(f"Ошибка авторизации: {e}")
    # Вывод: Ошибка авторизации: Аутентификация не удалась,
    # пожалуйста, проверьте переданные логин и пароль
```

**Причины возникновения:**

- Неверные учетные данные (логин/пароль)
- Истек срок действия токена
- Проблемы с сетью при авторизации

### CdekRequestException

Исключение, возникающее при ошибках выполнения запросов к API.

```python
from cdek.exceptions import CdekRequestException

try:
    # Попытка получить несуществующий заказ
    client.order.get_by_uuid("00000000-0000-0000-0000-000000000000")
except CdekRequestException as e:
    print(f"Ошибка запроса: {e}")
    print(f"Код ответа HTTP: {e.status_code}")
    print(f"Ответ API: {e.response}")
```

**Свойства исключения:**

- `status_code` - HTTP код ответа
- `response` - полный ответ API в виде словаря

**Причины возникновения:**

- Неверные параметры запроса
- Сущность не найдена (404)
- Некорректные данные в запросе
- Ошибки валидации API
- Проблемы с сетью

## Примеры обработки ошибок

### Обработка ошибок при создании заказа

```python
from cdek.exceptions import CdekRequestException

try:
    order = OrderRequest(
        number="ORDER-001",
        tariff_code=999,  # Несуществующий тариф
        # ... остальные параметры
    )
    response = client.order.create(order)
except CdekRequestException as e:
    if e.status_code == 400:
        print("Ошибка валидации данных заказа")
        if e.response and "errors" in e.response:
            for error in e.response["errors"]:
                print(f"Код ошибки: {error.get('code')}")
                print(f"Сообщение: {error.get('message')}")
    elif e.status_code == 404:
        print("Ресурс не найден")
    else:
        print(f"Неожиданная ошибка: {e}")
```

### Обработка ошибок при получении заказа

```python
def get_order_safe(uuid: str):
    """Безопасное получение заказа с обработкой ошибок"""
    try:
        return client.order.get_by_uuid(uuid)
    except CdekRequestException as e:
        if e.status_code == 404:
            print(f"Заказ {uuid} не найден")
            return None
        elif e.status_code == 403:
            print(f"Нет доступа к заказу {uuid}")
            return None
        else:
            print(f"Ошибка при получении заказа: {e}")
            raise
    except CdekAuthException as e:
        print(f"Ошибка авторизации: {e}")
        raise
    except Exception as e:
        print(f"Неожиданная ошибка: {e}")
        raise

# Использование
order = get_order_safe("some-uuid")
if order:
    print(f"Заказ найден: {order.entity.uuid}")
```

### Обработка сетевых ошибок

```python
import time
from cdek.exceptions import CdekRequestException

def request_with_retry(func, max_retries=3, delay=1):
    """Выполнение запроса с повторными попытками"""
    for attempt in range(max_retries):
        try:
            return func()
        except CdekRequestException as e:
            # Проверяем, является ли это сетевой ошибкой
            if "Ошибка сети" in str(e) and attempt < max_retries - 1:
                wait_time = delay * (2 ** attempt)  # Экспоненциальная задержка
                print(f"Сетевая ошибка, повтор через {wait_time} сек...")
                time.sleep(wait_time)
            else:
                raise
    return None

# Использование
def get_order():
    return client.order.get_by_uuid("some-uuid")

order = request_with_retry(get_order, max_retries=3)
```

## Коды ошибок API

Библиотека автоматически переводит коды ошибок API на русский язык. Все доступные коды ошибок находятся в `constants.ERRORS`:

```python
from cdek import constants

# Просмотр всех кодов ошибок
for code, message in constants.ERRORS.items():
    print(f"{code}: {message}")
```

### Основные коды ошибок:

- `v2_entity_not_found` - Сущность не найдена
- `v2_bad_request` - Некорректный запрос
- `v2_field_is_empty` - Не передано обязательное поле
- `v2_invalid_format` - Некорректное значение
- `v2_order_not_found` - Заказ не найден
- `v2_order_forbidden` - Заказ принадлежит другому клиенту

## Логирование ошибок

### Настройка логирования

```python
import logging

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

try:
    order = client.order.create(order_request)
    logger.info(f"Заказ создан: {order.entity.uuid}")
except CdekRequestException as e:
    logger.error(f"Ошибка создания заказа: {e}")
    logger.error(f"Код ответа: {e.status_code}")
    logger.error(f"Ответ API: {e.response}")
except CdekAuthException as e:
    logger.error(f"Ошибка авторизации: {e}")
except Exception as e:
    logger.exception("Неожиданная ошибка", exc_info=True)
```

## Валидация данных перед отправкой

### Проверка обязательных полей

```python
def validate_order(order: OrderRequest) -> list[str]:
    """Валидация заказа перед отправкой"""
    errors = []

    if not order.number:
        errors.append("Не указан номер заказа")

    if not order.tariff_code:
        errors.append("Не указан код тарифа")

    if not order.from_location:
        errors.append("Не указан адрес отправителя")

    if not order.to_location:
        errors.append("Не указан адрес получателя")

    if not order.packages or len(order.packages) == 0:
        errors.append("Не указаны упаковки")

    return errors

# Использование
order = OrderRequest(...)
errors = validate_order(order)

if errors:
    print("Ошибки валидации:")
    for error in errors:
        print(f"- {error}")
else:
    try:
        response = client.order.create(order)
        print(f"Заказ создан: {response.entity.uuid}")
    except CdekRequestException as e:
        print(f"Ошибка API: {e}")
```

## Обработка частичных ошибок

При работе с несколькими заказами может возникнуть ситуация, когда часть запросов выполняется успешно, а часть - с ошибками:

```python
def create_orders_batch(orders: list[OrderRequest]) -> dict:
    """Создание нескольких заказов с обработкой ошибок"""
    results = {
        "success": [],
        "failed": []
    }

    for order in orders:
        try:
            response = client.order.create(order)
            results["success"].append({
                "im_number": order.number,
                "cdek_uuid": response.entity.uuid
            })
        except CdekRequestException as e:
            results["failed"].append({
                "im_number": order.number,
                "error": str(e),
                "status_code": e.status_code,
                "response": e.response
            })
        except Exception as e:
            results["failed"].append({
                "im_number": order.number,
                "error": f"Неожиданная ошибка: {e}"
            })

    return results

# Использование
orders = [order1, order2, order3]
results = create_orders_batch(orders)

print(f"Успешно создано: {len(results['success'])}")
print(f"Ошибок: {len(results['failed'])}")

for failed in results["failed"]:
    print(f"Заказ {failed['im_number']}: {failed['error']}")
```
