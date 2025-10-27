"""
Класс MoneyResponse для ответов от API
"""

from .source import Source
from ...mixin.money import Money as MoneyMixin
from dataclasses import dataclass


@dataclass
class MoneyResponse(Source, MoneyMixin):
    """Класс для ответа о money"""

