"""
Класс CitiesResponse для ответов от API
"""
from .source import Source
from ..mixin.location import Location


class CitiesResponse(Source, Location):
    """Класс для ответа о городах"""


    time_zone: str | None = None
    payment_limit: str | None = None
