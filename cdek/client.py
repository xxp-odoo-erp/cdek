import time
import requests
from typing import Optional, Callable, Any, Dict
from . import constants
from .exceptions import CdekAuthException, CdekRequestException
from .responses.tariff import TariffResponse
from .responses.tariff_list_response import TariffListResponse
from .responses.entity import EntityResponse
from .responses.print_response import PrintResponse
from .responses.order import OrderResponse
from .responses.registry import RegistryResponse
from .responses.payment_response import PaymentResponse
from .responses.agreement_response import AgreementResponse
from .responses.intakes_response import IntakesResponse
from .responses.check_response import CheckResponse
from .responses.webhook_list_response import WebhookListResponse
from .requests.currency_enum import CurrencyEnum

def prepare_json_response(properties: dict | None = None) -> dict:
    if properties is None:
        return None
    # Обработка структуры с 'entity'
    if 'entity' in properties and isinstance(properties['entity'], (dict, list)):
        entity_data = properties['entity']
        # Проверяем если это список
        if isinstance(entity_data, list) and len(entity_data) > 1:
            if 'requests' in properties:
                entity_data[0]['requests'] = properties.get('requests', [])
            properties = entity_data[0]
        elif isinstance(entity_data, dict):
            # Копируем данные из entity
            entity_dict = entity_data.copy()
            # Добавляем requests если есть на верхнем уровне
            if 'requests' in properties and 'requests' not in entity_dict:
                entity_dict['requests'] = properties.get('requests', [])
            if 'related_entities' in properties and 'related_entities' not in entity_dict:
                entity_dict['related_entities'] = properties.get('related_entities', [])
            properties = entity_dict

    # Обработка структуры type.entity
    elif 'type' in properties and isinstance(properties['type'], dict):
        type_data = properties['type']
        if 'entity' in type_data and isinstance(type_data['entity'], dict):
            # Берем данные из type.entity
            entity_data = type_data['entity'].copy()
            # Добавляем requests если есть
            if 'requests' in type_data:
                entity_data['requests'] = type_data['requests']
            if 'related_entities' in type_data:
                entity_data['related_entities'] = type_data.get('related_entities', [])
            # Используем entity_data для заполнения
            properties = entity_data
    return properties

def prepare_query_params(filter_params: dict | None = None, valid_params: list | None = None) -> dict:
    params = {}
    if filter_params is None or valid_params is None:
        return None
    if not (filter_params and isinstance(filter_params, dict)):
        return None
    for key in filter_params.keys():
        if key in valid_params:
            params[key] = filter_params[key]
        else:
            raise KeyError(f"Неизвестный параметр: {key}")
    return params


class CdekClient:
    """Клиент взаимодействия с API CDEK 2.0"""

    def __init__(self, account: str, secure: Optional[str] = None, timeout: float = 5.0):
        """
        Конструктор клиента

        Args:
            account: Логин Account в сервисе Интеграции
            secure: Пароль Secure password в сервисе Интеграции
            timeout: Настройка клиента задающая общий тайм-аут запроса в секундах
        """
        if account == 'TEST':
            self.base_url = constants.API_URL_TEST
            self.account = constants.TEST_ACCOUNT
            self.secure = constants.TEST_SECURE
            self.account_type = 'TEST'
        else:
            self.base_url = constants.API_URL
            self.account = account
            self.secure = secure
            self.account_type = 'COMBAT'

        self.timeout = timeout
        self.token = None
        self.expire = 0
        self.memory = None
        self.memory_save_callback = None

        # Создаём сессию для повторного использования соединений
        self._session = requests.Session()

    def set_memory(self, memory: Optional[Dict], save_callback: Callable) -> 'CdekClient':
        """
        Установить параметры сохранения токена

        Args:
            memory: массив настройки сохранения
            save_callback: коллбэк сохранения

        Returns:
            self
        """
        self.memory = memory
        self.memory_save_callback = save_callback
        return self

    def _api_request(self, method: str, url: str, params: Optional[Any] = None) -> Dict:
        """
        Выполнить запрос к API

        Args:
            method: Метод запроса (GET, POST, PATCH, DELETE)
            url: URL path запроса
            params: параметры запроса

        Returns:
            ответ от API

        Raises:
            CdekRequestException: в случае ошибки запроса
        """
        # Авторизуемся или получаем данные из кэша
        if not self._check_saved_token():
            self._authorize()

        # Проверяем является ли запрос на файл pdf
        is_pdf_file_request = '.pdf' in url

        headers = {
            'Authorization': f'Bearer {self.token}'
        }

        if is_pdf_file_request:
            headers['Accept'] = 'application/pdf'
        else:
            headers['Accept'] = 'application/json'

        # Подготовка параметров
        if params is not None:
            if hasattr(params, 'prepare_request'):
                request_params = params.prepare_request()
            elif isinstance(params, dict):
                request_params = params
            else:
                request_params = params
        else:
            request_params = None

        try:
            if method == 'GET':
                response = self._session.get(
                    f'{self.base_url}{url}',
                    params=request_params,
                    headers=headers,
                    timeout=self.timeout
                )
            elif method == 'POST':
                response = self._session.post(
                    f'{self.base_url}{url}',
                    json=request_params,
                    headers=headers,
                    timeout=self.timeout
                )
            elif method == 'PATCH':
                response = self._session.patch(
                    f'{self.base_url}{url}',
                    json=request_params,
                    headers=headers,
                    timeout=self.timeout
                )
            elif method == 'DELETE':
                response = self._session.delete(
                    f'{self.base_url}{url}',
                    headers=headers,
                    timeout=self.timeout
                )
            else:
                raise ValueError(f"Неподдерживаемый метод: {method}")

            # Если запрос на PDF
            if is_pdf_file_request:
                if response.status_code == 200:
                    content_type = response.headers.get('Content-Type', '')
                    if 'application/pdf' in content_type:
                        return response.content
                # Если не PDF, продолжаем обработку как обычный ответ

            # Парсим JSON ответ
            if response.text:
                api_response = prepare_json_response(response.json())
            else:
                api_response = {}

            # Проверяем ошибки
            self._check_errors(url, response, api_response)

            # Возвращаем PDF если это PDF запрос
            if is_pdf_file_request and response.status_code == 200:
                return response.content

            return api_response

        except requests.exceptions.RequestException as e:
            raise CdekRequestException(f"Ошибка сети при вызове метода {url}: {str(e)}") from e

    def _authorize(self) -> bool:
        """
        Авторизация клиента в сервисе Интеграции

        Raises:
            CdekAuthException: в случае ошибки авторизации
        """
        params = {
            constants.AUTH_KEY_TYPE: constants.AUTH_PARAM_CREDENTIAL,
            constants.AUTH_KEY_CLIENT_ID: self.account,
            constants.AUTH_KEY_SECRET: self.secure,
        }

        headers = {'Content-Type': 'application/x-www-form-urlencoded'}

        try:
            response = self._session.post(
                f'{self.base_url}{constants.OAUTH_URL}',
                data=params,
                headers=headers,
                timeout=self.timeout
            )

            if response.status_code == 200:
                token_info = response.json()
                self.token = token_info.get('access_token', '')
                expires_in = token_info.get('expires_in', 0)
                self.expire = int(time.time()) + expires_in - 10

                if self.memory_save_callback is not None:
                    self._save_token(self.memory_save_callback)

                return True
            else:
                raise CdekAuthException(constants.AUTH_FAIL)

        except requests.exceptions.RequestException as e:
            raise CdekAuthException(f"{constants.AUTH_FAIL}: {str(e)}") from e

    def _check_saved_token(self) -> bool:
        """Проверить сохранённый токен"""
        check_memory = self.memory

        # Если не передан верный сохранённый массив данных для авторизации
        if not check_memory or 'account_type' not in check_memory or \
           'expires_in' not in check_memory or 'access_token' not in check_memory:
            return False

        # Проверяем тип аккаунта
        if check_memory.get('account_type') != self.account_type:
            return False

        # Проверяем срок действия токена
        if check_memory['expires_in'] > time.time() and check_memory.get('access_token'):
            self.token = check_memory['access_token']
            return True

        return False

    def _save_token(self, callback: Callable):
        """Сохранить токен через коллбэк"""
        callback({
            'cdekAuth': {
                'expires_in': self.expire,
                'access_token': self.token,
                'account_type': self.account_type,
            }
        })

    def _check_errors(self, method: str, response: requests.Response, api_response: Dict):
        """
        Проверить ответ на ошибки

        Args:
            method: URL метода
            response: HTTP ответ
            api_response: распарсенный JSON ответ

        Raises:
            CdekRequestException: в случае ошибки
        """
        if not api_response:
            raise CdekRequestException(
                f"От API CDEK при вызове метода {method} пришел пустой ответ",
                response.status_code
            )

        # Обработка ошибок с requests
        if response.status_code > 202 and 'requests' in api_response:
            if 'errors' in api_response['requests'][0] or \
               api_response['requests'][0].get('state') == 'INVALID':
                error_data = api_response['requests'][0]['errors'][0]
                message = CdekRequestException.get_translation(
                    error_data['code'],
                    error_data['message']
                )
                raise CdekRequestException(
                    f"От API CDEK при вызове метода {method} получена ошибка: {message}",
                    response.status_code
                )

        # Обработка общих ошибок
        if isinstance(api_response, dict) and \
           (('errors' in api_response and response.status_code == 200) or \
            (api_response.get('state') == 'INVALID') or \
            ('errors' in api_response and response.status_code != 200)):
            error_data = api_response['errors'][0]
            message = CdekRequestException.get_translation(
                error_data['code'],
                error_data['message']
            )
            raise CdekRequestException(
                f"От API CDEK при вызове метода {method} получена ошибка: {message}",
                response.status_code
            )

        # Общая ошибка при неверном статусе
        if response.status_code > 202 and 'requests' not in api_response:
            raise CdekRequestException(
                f"Неверный код ответа от сервера CDEK при вызове метода {method}: {response.status_code}",
                response.status_code
            )

    def get_currency(self, currency_code: str) -> int:
        """Get currency code by name"""
        try:
            return CurrencyEnum[currency_code].value
        except ValueError:
            raise CdekRequestException(f"Неизвестный код валюты: {currency_code}")

    # Методы API

    def get_regions(self, filter_params=None):
        """Получение списка регионов"""
        if filter_params and hasattr(filter_params, 'regions'):
            filter_params.regions()
            params = filter_params
        else:
            params = None
        params = prepare_query_params(filter_params, constants.REGIONS_FILTER)
        response = self._api_request('GET', constants.REGIONS_URL, params)
        # Здесь должен быть импорт и создание RegionsResponse объектов
        return response

    def get_cities(self, filter_params: dict | None=None):
        """Получение списка городов"""
        # Обрабатываем filter_params как словарь
        params = prepare_query_params(filter_params, constants.CITIES_FILTER)
        response = self._api_request('GET', constants.CITIES_URL, params)

        # Если это список, возвращаем как есть
        if isinstance(response, list):
            return response

        # Если это словарь с 'location', возвращаем список городов
        if isinstance(response, dict) and 'location' in response:
            # Возвращаем список locations
            locations = response['location']
            if isinstance(locations, list):
                return locations

        return response

    def get_delivery_points(self, filter_params=None):
        """Получение списка ПВЗ СДЭК"""
        params = prepare_query_params(filter_params, constants.DELIVERY_POINTS_FILTER)
        response = self._api_request('GET', constants.DELIVERY_POINTS_URL, params)
        # Здесь должен быть импорт и создание DeliveryPointsResponse объектов
        return response

    def calculate_tariff(self, tariff):
        """Расчёт стоимости и сроков доставки по коду тарифа"""
        if not tariff.get_tariff_code():
            raise ValueError('Не установлен обязательный параметр tariff_code')
        response = self._api_request('POST', constants.CALC_TARIFF_URL, tariff)
        return TariffResponse(**response)

    def calculate_tariff_list(self, tariff):
        """Расчёт стоимости и сроков доставки по всем доступным тарифам

        Args:
            tariff: объект Tariff с параметрами запроса (type, from_location, to_location, packages)

        Returns:
            Список объектов TariffListResponse с информацией о доступных тарифах
        """
        response = self._api_request('POST', constants.CALC_TARIFFLIST_URL, tariff)

        # API возвращает словарь с ключом "tariff_codes" содержащим список тарифов
        if isinstance(response, dict) and 'tariff_codes' in response:
            tariff_codes = response['tariff_codes']
            if isinstance(tariff_codes, list):
                return [TariffListResponse(**item) for item in tariff_codes]

        # Если это список тарифов напрямую
        if isinstance(response, list):
            return [TariffListResponse(**item) for item in response]

        # Если это словарь с одним тарифом
        if isinstance(response, dict):
            return [TariffListResponse(**response)]

        # Если это список с одним элементом или пустой список
        return []

    def create_order(self, order):
        """Создание заказа"""
        response = self._api_request('POST', constants.ORDERS_URL, order)
        return EntityResponse(**response)

    def delete_order(self, uuid: str) -> bool:
        """Удалить заказ по uuid"""
        try:
            response = self._api_request('DELETE', f'{constants.ORDERS_URL}/{uuid}')
            request = EntityResponse(**response)
            requests_list = request.get_requests()

            # Логируем для отладки
            if requests_list and len(requests_list) > 0:
                first_request = requests_list[0]
                # Поддерживаем как объекты RequestResponse, так и словари
                if isinstance(first_request, dict):
                    state = first_request.get('state')
                else:
                    state = first_request.get_state()

                # Проверяем результат
                # По документации API, успешное удаление возвращает state != 'INVALID'
                return state != 'INVALID' if state else False

            # Если нет requests, проверяем есть ли entity в ответе
            # Иногда API возвращает пустой успешный ответ
            if hasattr(request, 'requests') and len(request.requests) == 0:
                # Пустой список requests может означать успех
                return True

            return False
        except CdekRequestException as e:
            error_str = str(e)
            # Если заказ не найден (404), это тоже успех - заказ удалён или не существовал
            if 'не существует' in error_str or 'not found' in error_str.lower() or 'Entity is not found' in error_str:
                return True
            # Если заказ в состоянии INVALID - нельзя удалить (ограничение API)
            if 'invalid' in error_str.lower() or 'некорректна' in error_str.lower() or 'Entity is invalid' in error_str:
                # Возвращаем False, так как удаление не удалось
                # Но это не ошибка для тестовой среды
                raise CdekRequestException(
                    f"Заказ {uuid} находится в состоянии INVALID и не может быть удален (см. https://apidoc.cdek.ru/#tag/order/operation/delete)",
                    None
                )
            raise

    def cancel_order(self, order_uuid: str):
        """Регистрация отказа"""
        response = self._api_request('POST', f'{constants.ORDERS_URL}/{order_uuid}/refusal')
        return EntityResponse(**response)

    def update_order(self, order):
        """Обновление заказа"""
        response = self._api_request('PATCH', constants.ORDERS_URL, order)
        return EntityResponse(**response)

    def get_order_info_by_cdek_number(self, cdek_number: str):
        """Полная информация о заказе по трек номеру"""
        response = self._api_request('GET', constants.ORDERS_URL, {'cdek_number': cdek_number})
        return OrderResponse(**response)

    def get_order_info_by_im_number(self, im_number: str):
        """Полная информация о заказе по ID заказа в магазине"""
        response = self._api_request('GET', constants.ORDERS_URL, {'im_number': im_number})
        return OrderResponse(**response)

    def get_order_info_by_uuid(self, uuid: str):
        """Полная информация о заказе по uuid"""
        response = self._api_request('GET', f'{constants.ORDERS_URL}/{uuid}')
        return OrderResponse(**response)

    def set_barcode(self, barcode):
        """Запрос на формирование ШК-места к заказу"""
        response = self._api_request('POST', constants.BARCODES_URL, barcode)
        return EntityResponse(**response)

    def get_barcode(self, uuid: str):
        """Получение сущности ШК к заказу"""
        response = self._api_request('GET', f'{constants.BARCODES_URL}/{uuid}')
        return PrintResponse(**response)

    def get_barcode_pdf(self, uuid: str):
        """Получение PDF ШК-места к заказу"""
        return self._api_request('GET', f'{constants.BARCODES_URL}/{uuid}.pdf')

    def get_invoice_pdf(self, uuid: str):
        """Получение PDF накладной к заказу"""
        return self._api_request('GET', f'{constants.INVOICE_URL}/{uuid}.pdf')

    def set_invoice(self, invoice):
        """Запрос на формирование накладной к заказу"""
        response = self._api_request('POST', constants.INVOICE_URL, invoice)
        return EntityResponse(**response)

    def get_invoice(self, uuid: str):
        """Получение сущности накладной к заказу"""
        response = self._api_request('GET', f'{constants.INVOICE_URL}/{uuid}')
        return PrintResponse(**response)

    def get_registries(self, date: str):
        """Запрос на получение информации о реестрах НП"""
        try:
            response = self._api_request('GET', 'registries', {'date': date})
            return RegistryResponse(**response)
        except CdekRequestException as e:
            # Пустой ответ - это нормальная ситуация, когда нет реестров за указанную дату
            if 'пустой ответ' in str(e).lower() or 'пустой ответ' in str(e):
                return RegistryResponse()
            raise

    def get_payments(self, date: str):
        """Запрос на получение информации о переводе наложенного платежа"""
        try:
            response = self._api_request('GET', 'payment', {'date': date})
            return PaymentResponse(**response)
        except CdekRequestException as e:
            # Пустой ответ - это нормальная ситуация, когда нет переводов за указанную дату
            if 'пустой ответ' in str(e).lower() or 'пустой ответ' in str(e):
                return PaymentResponse()
            raise

    def create_agreement(self, agreement):
        """Создание договоренностей для курьера"""
        response = self._api_request('POST', constants.COURIER_AGREEMENTS_URL, agreement)
        return AgreementResponse(**response)

    def get_agreement(self, uuid: str):
        """Получение договоренностей для курьера"""
        response = self._api_request('GET', f'{constants.COURIER_AGREEMENTS_URL}/{uuid}')
        return AgreementResponse(**response)

    def create_intakes(self, intakes):
        """Создание заявки на вызов курьера"""
        response = self._api_request('POST', constants.INTAKES_URL, intakes)
        return EntityResponse(**response)

    def get_intakes(self, uuid: str):
        """Информация о заявке на вызов курьера"""
        response = self._api_request('GET', f'{constants.INTAKES_URL}/{uuid}')
        return IntakesResponse(**response)

    def delete_intakes(self, uuid: str) -> bool:
        """Удаление заявки на вызов курьера"""
        try:
            self._api_request('DELETE', f'{constants.INTAKES_URL}/{uuid}')
            return True
        except CdekRequestException as e:
            # Если заявка не найдена (404), это тоже успех - заявка удалена или не существовала
            error_str = str(e)
            if 'не существует' in error_str or 'not found' in error_str.lower() or 'Entity is not found' in error_str:
                return True
            raise

    def get_checks(self, check):
        """Метод используется для получения информации о чеке по заказу или за выбранный день"""
        response = self._api_request('GET', 'check', check)
        return CheckResponse(**response)

    def set_webhooks(self, webhooks):
        """Добавление нового слушателя webhook"""
        response = self._api_request('POST', constants.WEBHOOKS_URL, webhooks)
        return EntityResponse(**response)

    def get_webhooks(self):
        """Информация о слушателях webhook"""
        response = self._api_request('GET', constants.WEBHOOKS_URL)

        # Если это список, возвращаем массив объектов
        if isinstance(response, list):
            return [WebhookListResponse(**item) for item in response]

        # Если это один объект, оборачиваем в список
        return [WebhookListResponse(**response)]

    def get_webhook(self, uuid: str):
        """Информация о слушателе webhook"""
        response = self._api_request('GET', f'{constants.WEBHOOKS_URL}/{uuid}')
        return EntityResponse(**response)

    def delete_webhooks(self, uuid: str):
        """Удаление слушателя webhook"""
        response = self._api_request('DELETE', f'{constants.WEBHOOKS_URL}/{uuid}')
        return EntityResponse(**response)

