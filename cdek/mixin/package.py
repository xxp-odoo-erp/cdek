from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..entity.requests.item import Item

@dataclass
class Package:
    number: str | None = None
    weight: int | None = None
    length: int | None = None
    width: int | None = None
    height: int | None = None
    comment: str | None = None
    package_id: str | None = None
    items: 'list[Item] | None' = None

    def set_number(self, number: str):
        self.number = number
        return self

    def set_weight(self, weight: int):
        self.weight = weight
        return self

    def set_dimensions(self, length: int, width: int, height: int):
        self.length = length
        self.width = width
        self.height = height
        return self

    def set_comment(self, comment: str):
        self.comment = comment
        return self

    def add_item(self, item: 'Item'):
        if self.items is None:
            self.items = []
        self.items.append(item)
        return self