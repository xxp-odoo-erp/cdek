from .source import Source
from ..mixin.services import ServicesMixin
from dataclasses import dataclass

@dataclass
class Services(Source, ServicesMixin):
    """Класс для дополнительных услуг"""

