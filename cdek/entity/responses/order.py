from dataclasses import dataclass, field

from .source import Source
from ...mixin.order import Order as OrderMixin
from ...mixin.common import Common as CommonMixin
from ...mixin.tariff import Tariff as TariffMixin

@dataclass
class OrderResponse(Source, OrderMixin, CommonMixin, TariffMixin):
    """Класс для ответа о заказе"""

    is_return: bool | None = None
    is_reverse: bool | None = None
    delivery_mode: str | None = None
    delivery_problem: list | None = field(default_factory=list)
    delivery_detail: list | None = field(default_factory=list)
    transacted_payment: bool | None = None
    type: int | None = None
    tariff_code: str | None = None
    statuses: list | None = field(default_factory=list)
    related_entities: list | None = field(default_factory=list)
    requests: list | None = field(default_factory=list)
    services: list | None = field(default_factory=list)

    def __init__(self, properties=None):
        """Переопределяем __init__ чтобы вызвать родительский"""
        # Вызываем Source.__init__ напрямую
        Source.__init__(self, properties)

    def get_last_related(self, entity_type: str):
        """Получить последнюю связанную сущность"""
        newest = []
        if isinstance(self.related_entities, list):
            for entity in self.related_entities:
                if entity.get('type') == entity_type:
                    newest.append(entity)

        return newest[-1]['uuid'] if newest else None

    @staticmethod
    def withOrderUuid(order_uuid: str) -> 'OrderResponse':
        return OrderResponse(order_uuid=order_uuid)

    @staticmethod
    def withCdekNumber(cdek_number: str) -> 'OrderResponse':
        return OrderResponse(cdek_number=cdek_number)
