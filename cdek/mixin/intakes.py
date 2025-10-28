from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..requests.location import Location
    from ..requests.contact import Contact

@dataclass
class IntakesMixin:
    """Mixin for courier pickup requests."""
    
    intake_date: str | None = None
    intake_time_from: str | None = None
    intake_time_to: str | None = None
    lunch_time_from: str | None = None
    lunch_time_to: str | None = None
    name: str | None = None
    need_call: bool | None = None
    from_location: 'Location | None' = None
    sender: 'Contact | None' = None
