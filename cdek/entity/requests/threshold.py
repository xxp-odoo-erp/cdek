"""
Класс Threshold для запросов к API
"""

from .source import Source
from ...mixin.threshold import Threshold as ThresholdMixin
from dataclasses import dataclass

@dataclass
class Threshold(Source, ThresholdMixin):
    """Класс для порога доставки"""
