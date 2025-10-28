"""
Класс ContactResponse для ответов от API
"""

from dataclasses import dataclass
from .source import Source
from ...mixin.contact import Contact as ContactMixin

@dataclass
class ContactResponse(Source, ContactMixin):
    pass
