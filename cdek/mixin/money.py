from dataclasses import dataclass
from .express import Express

@dataclass
class Money(Express):
    value: float | None = None
    vat_sum: float | None = None
    vat_rate: int | None = None
