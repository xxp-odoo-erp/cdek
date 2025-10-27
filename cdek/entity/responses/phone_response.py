"""
Класс PhoneResponse для ответов от API
"""

from .source import Source
from ...mixin.phone import Phone as PhoneMixin
from dataclasses import dataclass

@dataclass
class PhoneResponse(Source, PhoneMixin):
    """Класс для ответа о phone"""

