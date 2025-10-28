from .source import Source
from dataclasses import dataclass

@dataclass
class OfficeImageResponse(Source):
    """Класс для ответа о officeimage"""

    url: str | None = None
    number: int | None = None
