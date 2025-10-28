"""
Класс RequestsResponse для ответов от API
"""
from dataclasses import dataclass
from .source import Source


@dataclass
class RequestsResponse(Source):
    """Класс для ответа о requests"""

