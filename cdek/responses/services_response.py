from .source import Source
from dataclasses import dataclass
from ..mixin.services import ServicesMixin  # noqa: F401

@dataclass
class ServicesResponse(Source, ServicesMixin):
    """Класс для ответа о services"""
    sum: float | None = None
