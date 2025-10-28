from dataclasses import dataclass
from .express import ExpressMixin

@dataclass
class PhoneMixin(ExpressMixin):
    """Mixin for phone number data."""
    
    number: str | None = None
    additional: str | None = None
