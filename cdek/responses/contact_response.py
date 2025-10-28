from dataclasses import dataclass
from .source import Source
from ..mixin.contact import ContactMixin

@dataclass
class ContactResponse(Source, ContactMixin):
    pass
