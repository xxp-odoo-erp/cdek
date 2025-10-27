"""
Класс SellerResponse для ответов от API
"""

from .source import Source
from dataclasses import dataclass
from ...mixin.seller import Seller as SellerMixin  # noqa: F401

@dataclass
class SellerResponse(Source, SellerMixin):
    """Класс для ответа о seller"""

