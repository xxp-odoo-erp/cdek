from enum import IntEnum

from cdek.apps.app import App
from cdek.exceptions import CdekRequestException


class Currency(IntEnum):
    """Enum для кодов валют, используемых в методах расчета стоимости CDEK."""

    RUB = 1  # Российский рубль
    KZT = 2  # Тенге
    USD = 3  # Доллар США
    EUR = 4  # Евро
    GBP = 5  # Фунт Стерлингов
    CNY = 6  # Китайский юань
    BYR = 7  # Белорусский рубль
    UAH = 8  # Гривна
    KGS = 9  # Киргизский сом
    AMD = 10  # Армянский драм
    TRY = 11  # Турецкая лира
    THB = 12  # Тайский бат
    KRW = 13  # Вон
    AED = 14  # Дирхам
    UZS = 15  # Узбекский сум
    MNT = 16  # Тугрик
    PLN = 17  # Злотый
    AZN = 18  # Манат
    GEL = 19  # Лари
    JPY = 55  # Йена
    VND = 704  # Вьетнамский донг


class CurrencyApp(App):
    def get(self, currency_code: str) -> int:
        """Получить числовой код валюты по её символьному обозначению"""
        try:
            return Currency[currency_code].value
        except ValueError as e:
            raise CdekRequestException(
                f"Неизвестный код валюты: {currency_code}"
            ) from e

    def all(self) -> list[int]:
        """Получить список всех поддерживаемых кодов валют"""
        return [currency.value for currency in Currency]
