from dataclasses import dataclass

from .order import Order
from .source import Source

@dataclass
class Invoice(Source):
    """Класс для квитанции к заказу"""


    orders: list | None = None
    copy_count: int = 1
    type: str | None = None

    def __post_init__(self):
        """Инициализация после создания"""
        if self.orders is None:
            self.orders = []

    def add_order(self, order: Order):
        """Установить список заказов"""
        self.orders.append(order)
        return self

    def set_copy_count(self, copy_count: int = 1):
        """Установить число копий"""
        self.copy_count = copy_count
        return self

    def set_type(self, invoice_type: str):
        """Установить форму квитанции"""
        self.type = invoice_type
        return self

    @classmethod
    def with_orders_uuid(cls, orders_uuid):
        """Экспресс-метод: создать с UUID заказов"""
        instance = cls()
        if not instance.orders:
            instance.orders = []

        if isinstance(orders_uuid, list):
            for order_uuid in orders_uuid:
                order_obj = Order()
                order_obj.order_uuid = order_uuid  # Используем order_uuid вместо uuid
                instance.orders.append(order_obj)
        else:
            instance.orders.append(Order.with_cdek_number(orders_uuid))
        return instance

