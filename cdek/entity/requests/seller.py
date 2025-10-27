"""
Класс Seller для запросов к API
"""

from .source import Source
from ...mixin.seller import Seller as SellerMixin
from dataclasses import dataclass

@dataclass
class Seller(Source, SellerMixin):
    """Класс для реквизитов продавца"""
