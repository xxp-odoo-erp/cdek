from dataclasses import dataclass
from .source import Source


@dataclass
class DeliveryDetailResponse(Source):
    date: str | None = None
    recipient_name: str | None = None
    payment_sum: float | None = None
    payment_info: dict | None = None
    delivery_sum: float | None = None
    total_sum: float | None = None
