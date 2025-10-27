from dataclasses import dataclass
from .source import Source
from ...mixin.item import Item as ItemMixin


@dataclass
class ItemsResponse(Source, ItemMixin):

    delivery_amount: int | None = None
