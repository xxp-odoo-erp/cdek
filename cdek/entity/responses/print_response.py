"""
Класс PrintResponse для ответов от API
"""

from .entity import EntityResponse
from .order import OrderResponse
from .statuses_response import StatusesResponse

class PrintResponse(EntityResponse):
    """Класс для печатной формы"""

    def get_order_uuid(self) -> list | None:
        orders = []
        if self.entity.get('orders'):
            for order in self.entity['orders']:
                if order.get('order_uuid'):
                    orders.append(OrderResponse.withOrderUuid(order['order_uuid']))
                if order.get('cdek_number'):
                    orders.append(OrderResponse.withCdekNumber(order['cdek_number']))
        return orders

    def get_url(self) -> str | None:
        return self.entity.get('url')

    def get_copy_count(self) -> int | None:
        if self.entity.get('copy_count'):
            return self.entity['copy_count']

    def get_lang(self) -> str | None:
        if self.entity.get('lang'):
            return self.entity['lang']

    def get_format(self) -> str | None:
        if self.entity.get('format'):
            return self.entity['format']

    def get_statuses(self) -> list | None:
        if self.entity.get('statuses'):
            return [StatusesResponse(status) for status in self.entity['statuses']]
