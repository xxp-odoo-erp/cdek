from dataclasses import dataclass
from .source import Source
from ..mixin.tariff import TariffMixin


@dataclass
class Tariff(Source, TariffMixin):
    """Класс для расчёта тарифа"""

    date: str | None = None
    currency: int | None = None
    lang: str | None = None
