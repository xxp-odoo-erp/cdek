"""
Класс ThresholdResponse для ответов от API
"""

from .source import Source
from dataclasses import dataclass
from ...mixin.threshold import Threshold as ThresholdMixin  # noqa: F401

@dataclass
class ThresholdResponse(Source, ThresholdMixin):
    """Класс для ответа о threshold"""

