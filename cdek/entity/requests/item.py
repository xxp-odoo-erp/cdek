from dataclasses import dataclass
from .source import Source
from ...mixin.item import Item as ItemMixin

@dataclass
class Item(Source, ItemMixin):
    """Класс для товара в заказе"""
