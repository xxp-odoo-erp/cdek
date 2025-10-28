from dataclasses import dataclass
from .source import Source
from ..mixin.location import LocationMixin


@dataclass
class CitiesResponse(Source, LocationMixin):
    """Класс для ответа о городах"""


    time_zone: str | None = None
    payment_limit: str | None = None
