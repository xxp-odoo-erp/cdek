"""
Класс RegionsResponse для ответов от API
"""

from .source import Source
from dataclasses import dataclass

@dataclass
class RegionsResponse(Source):
    """Класс для ответа о regions"""

    country: str | None = None
    country_code: str | None = None
    region: str | None = None
    region_code: int | None = None
