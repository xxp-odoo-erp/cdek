from dataclasses import dataclass
from .source import Source
from ...mixin.contact import Contact as ContactMixin

@dataclass
class Contact(Source, ContactMixin):
    """Класс для работы с контактом"""
