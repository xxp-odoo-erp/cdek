"""
Класс Money для запросов к API
"""
from dataclasses import dataclass
from .source import Source
from ...mixin.money import Money as MoneyMixin


@dataclass
class Money(Source, MoneyMixin):
    """Класс для работы с денежными суммами"""

