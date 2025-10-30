from dataclasses import dataclass, field

from .source import Source


@dataclass
class Tariff(Source):

    tariff_code: int | None = None
    tariff_name: str | None = None
    tariff_description: str | None = None
    delivery_mode: int | None = None
    delivery_sum: float | None = None
    period_min: int | None = None
    period_max: int | None = None
    calendar_min: int | None = None
    calendar_max: int | None = None
    delivery_date_range: dict | None = None

    def get_delivery_sum(self):
        """Получить стоимость доставки"""
        return self.delivery_sum

    def get_period_min(self):
        """Получить минимальный период доставки"""
        return self.period_min

    def get_period_max(self):
        """Получить максимальный период доставки"""
        return self.period_max

    def get_tariff_code(self):
        """Получить код тарифа"""
        return self.tariff_code

    def get_tariff_name(self):
        """Получить название тарифа"""
        return self.tariff_name

    def get_tariff_description(self):
        """Получить описание тарифа"""
        return self.tariff_description

    def get_delivery_mode(self):
        """Получить режим доставки"""
        return self.delivery_mode


@dataclass
class TariffListResponse(Source):
    """Класс для ответа от API с информацией о тарифе"""

    tariff_codes: list[Tariff] | None = field(default_factory=list)