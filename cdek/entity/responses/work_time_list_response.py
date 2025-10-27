"""
Класс WorkTimeListResponse для ответов от API
"""

from .source import Source
from dataclasses import dataclass

@dataclass
class WorkTimeListResponse(Source):
    """Класс для ответа о worktimelist"""

    day: int | None = None
    time: int | None = None
