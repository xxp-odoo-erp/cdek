from dataclasses import dataclass
from .source import Source
from ..mixin.location import LocationMixin

@dataclass
class LocationResponse(Source, LocationMixin):
    """Класс для ответа о локации"""

    city_code: int | None = None
    address_full: str | None = None

    def get_city_code(self) -> int | None:
        return self.city_code

    def get_address_full(self) -> str | None:
        return self.address_full
