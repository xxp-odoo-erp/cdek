from dataclasses import dataclass

@dataclass
class DeliveryPointsMixin:
    """Mixin for delivery point filters."""
    
    have_cashless: bool | None = None
    have_cash: bool | None = None
    allowed_cod: bool | None = None
    is_dressing_room: bool | None = None
    is_handout: bool | None = None
    is_reception: bool | None = None
    weight_max: float | None = None
    weight_min: float | None = None
    take_only: bool | None = None
