from dataclasses import dataclass

from .source import Source
from .services_response import ServicesResponse

@dataclass
class TariffResponse(Source):
    """Класс для ответа о тарифе"""

    delivery_sum: float | None = None
    period_min: int | None = None
    period_max: int | None = None
    weight_calc: int | None = None
    total_sum: float | None = None
    currency: str | None = None
    services: list[ServicesResponse] | None = None

    def get_delivery_sum(self):
        """Получить стоимость доставки"""
        if isinstance(self.delivery_sum, dict):
            # Если delivery_sum это словарь со всеми данными, извлекаем значение
            return self.delivery_sum.get('delivery_sum')
        return self.delivery_sum

    def get_period_min(self):
        """Получить минимальный период доставки"""
        if isinstance(self.period_min, dict):
            return self.period_min.get('period_min')
        if isinstance(self.delivery_sum, dict):
            return self.delivery_sum.get('period_min')
        return self.period_min

    def get_period_max(self):
        """Получить максимальный период доставки"""
        if isinstance(self.period_max, dict):
            return self.period_max.get('period_max')
        if isinstance(self.delivery_sum, dict):
            return self.delivery_sum.get('period_max')
        return self.period_max

    def get_total_sum(self):
        """Получить общую стоимость"""
        if isinstance(self.total_sum, dict):
            return self.total_sum.get('total_sum')
        if isinstance(self.delivery_sum, dict):
            return self.delivery_sum.get('total_sum')
        return self.total_sum
