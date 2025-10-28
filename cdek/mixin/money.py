from dataclasses import dataclass
from .express import ExpressMixin

@dataclass
class MoneyMixin(ExpressMixin):
    """Mixin for working with monetary amounts and VAT."""
    
    value: float | None = None
    vat_sum: float | None = None
    vat_rate: int | None = None
