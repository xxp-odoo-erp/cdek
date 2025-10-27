"""
Класс Money для запросов к API
"""

from .source import Source
from ...mixin.money import Money as MoneyMixin


class Money(Source, MoneyMixin):
    """Класс для работы с денежными суммами"""

