from dataclasses import dataclass
from .source import Source
from ..mixin.common import CommonMixin

@dataclass
class Check(Source, CommonMixin):
    """Класс для получения информации о чеке"""

    date: str | None = None

