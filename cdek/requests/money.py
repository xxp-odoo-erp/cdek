from dataclasses import dataclass
from .source import Source
from ..mixin.money import MoneyMixin


@dataclass
class Money(Source, MoneyMixin):
    """Класс для работы с денежными суммами"""

