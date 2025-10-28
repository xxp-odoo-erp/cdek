from .source import Source
from dataclasses import dataclass, field

@dataclass
class PaymentResponse(Source):
    """Класс для ответа о платежах"""

    orders: list | None = field(default_factory=list)

    def get_orders(self) -> list | None:
        return self.orders
