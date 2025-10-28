from .source import Source
from ..mixin.threshold import ThresholdMixin
from dataclasses import dataclass

@dataclass
class Threshold(Source, ThresholdMixin):
    """Класс для порога доставки"""
