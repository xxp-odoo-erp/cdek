from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..entity.requests.contact import Contact

@dataclass
class Common:
    uuid: str | None = None
    order_uuid: str | None = None
    cdek_number: int | None = None
    sender: 'Contact | None' = None
    number: str | None = None
    comment: str | None = None

