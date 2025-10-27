from dataclasses import dataclass

from .money import Money
from .express import Express

@dataclass
class Threshold(Money, Express):

    threshold: int | None = None
    sum: float | None = None
