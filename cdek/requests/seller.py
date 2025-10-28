from .source import Source
from ..mixin.seller import SellerMixin
from dataclasses import dataclass

@dataclass
class Seller(Source, SellerMixin):
    """Класс для реквизитов продавца"""
