"""
Класс CitiesResponse для ответов от API
"""
from dataclasses import dataclass
from .source import Source
from ..mixin.location import Location


@dataclass
class CitiesResponse(Source, Location):
    """Класс для ответа о городах"""


    time_zone: str | None = None
    payment_limit: str | None = None
