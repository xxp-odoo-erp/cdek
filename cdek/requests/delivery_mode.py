from dataclasses import dataclass

from .source import Source

@dataclass
class DeliveryMode(Source):
    """Класс для работы с режимом доставки"""

    delivery_mode: str | None = None
    delivery_mode_name: str | None = None
    tariff_code: int | None = None
