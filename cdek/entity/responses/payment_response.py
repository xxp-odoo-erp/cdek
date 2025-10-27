"""
Класс PaymentResponse для ответов от API
"""

from .source import Source
from dataclasses import dataclass, field

@dataclass
class PaymentResponse(Source):
    """Класс для ответа о платежах"""

    orders: list | None = field(default_factory=list)

    def __init__(self, properties=None):
        """Переопределяем __init__ чтобы вызвать родительский"""
        Source.__init__(self, properties)

    def get_orders(self) -> list | None:
        return self.orders
