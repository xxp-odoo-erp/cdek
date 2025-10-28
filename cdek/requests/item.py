from dataclasses import dataclass
from .source import Source
from ..mixin.item import ItemMixin

@dataclass
class Item(Source, ItemMixin):
    """Класс для товара в заказе"""
