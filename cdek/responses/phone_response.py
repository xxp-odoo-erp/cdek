from .source import Source
from ..mixin.phone import PhoneMixin
from dataclasses import dataclass

@dataclass
class PhoneResponse(Source, PhoneMixin):
    """Класс для ответа о phone"""

