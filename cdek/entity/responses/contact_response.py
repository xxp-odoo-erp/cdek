"""
Класс ContactResponse для ответов от API
"""

from .source import Source
from ...mixin.contact import Contact as ContactMixin


class ContactResponse(Source, ContactMixin):
    pass
