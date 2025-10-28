from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..requests.contact import Contact

@dataclass
class CommonMixin:
    """Mixin for common order fields."""
    
    uuid: str | None = None
    order_uuid: str | None = None
    cdek_number: int | None = None
    sender: 'Contact | None' = None
    number: str | None = None
    comment: str | None = None

