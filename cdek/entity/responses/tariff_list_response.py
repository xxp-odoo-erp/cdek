"""
Класс TariffListResponse для ответов от API
"""

from .source import Source
from dataclasses import dataclass


@dataclass
class TariffListResponse(Source):
    """Класс для ответа от API"""

    delivery_mode: int | None = None
    tariff_name: str | None = None
    tariff_description: str | None = None
    tariff_code: int | None = None
    period_max: int | None = None
    period_min: int | None = None
    delivery_sum: float | None = None
