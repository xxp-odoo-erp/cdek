from .source import Source
from dataclasses import dataclass
from ..mixin.services import ServicesMixin  # noqa: F401

@dataclass
class ServicesResponse(Source, ServicesMixin):
    """Класс для ответа о services"""
    sum: float | None = None
    total_sum: float | None = None
    discount_percent: float | None = None
    discount_sum: float | None = None
    vat_rate: float | None = None
    vat_sum: float | None = None
