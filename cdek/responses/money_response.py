from .source import Source
from ..mixin.money import MoneyMixin
from dataclasses import dataclass


@dataclass
class MoneyResponse(Source, MoneyMixin):
    """Класс для ответа о money"""

