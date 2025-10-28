from dataclasses import dataclass
from .source import Source
from ..mixin.contact import ContactMixin

@dataclass
class Contact(Source, ContactMixin):
    """Класс для работы с контактом"""
