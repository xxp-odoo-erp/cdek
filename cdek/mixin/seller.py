from dataclasses import dataclass

@dataclass
class SellerMixin:
    """Mixin for seller information."""
    
    name: str | None = None
    inn: str | None = None
    phone: str | None = None
    ownership_form: int | None = None
    address: str | None = None
