from dataclasses import dataclass

from .money import MoneyMixin
from .express import ExpressMixin

@dataclass
class ThresholdMixin(MoneyMixin, ExpressMixin):
    """Mixin for working with payment thresholds."""
    
    threshold: int | None = None
    sum: float | None = None
