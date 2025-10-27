"""
CDEK Python SDK v2

Библиотека для работы с API СДЭК версии 2.

Пример использования:
    from cdekpy import CdekClient

    # Создание клиента для тестовой среды
    client = CdekClient('TEST')

    # Создание клиента для production
    client = CdekClient('PROD', account='your_account', secure_password='your_password')

    # Получение списка городов
    cities = client.get_cities({'size': 10})

    # Расчёт тарифа
    from cdekpy.entity.requests.tariff import Tariff
    tariff = Tariff()
    tariff.set_type(1)
    tariff.set_tariff_code(136)
    tariff.set_city_codes(44, 137)
    tariff.set_package_weight(1000)

    result = client.calculate_tariff(tariff)
"""

from .client import CdekClient
from .exceptions import CdekException, CdekAuthException, CdekRequestException
from . import constants

__version__ = "2.0.0"
__author__ = "CDEK Python SDK"
__license__ = "MIT"

__all__ = [
    'CdekClient',
    'CdekException',
    'CdekAuthException',
    'CdekRequestException',
    'constants',
]
