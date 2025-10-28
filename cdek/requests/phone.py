from dataclasses import dataclass
from .source import Source
from ..mixin.phone import PhoneMixin


@dataclass
class Phone(Source, PhoneMixin):
    pass
