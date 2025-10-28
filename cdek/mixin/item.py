from __future__ import annotations
from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..requests.money import Money

@dataclass
class ItemMixin:
    """Mixin for working with order items."""

    name: str | None = None
    ware_key: str | None = None
    marking: str | None = None
    payment: Money | None = None
    cost: float | None = None
    weight: int | None = None
    weight_gross: int | None = None
    amount: int | None = None
    name_i18n: str | None = None
    brand: str | None = None
    country_code: str | None = None
    material: int | None = None
    wifi_gsm: bool | None = None
    url: str | None = None
    feacn_code: str | None = None

    def set_payment(self, value: float, vat_sum: float | None = None, vat_rate: int | None = None):
        """Set payment amount with VAT."""
        from ..requests.money import Money  # noqa
        self.payment = Money.express({'value': value, 'vat_sum': vat_sum or 0, 'vat_rate': vat_rate or 20})
        return self

    def set_name(self, name: str):
        """Set item name."""
        self.name = name
        return self

    def set_ware_key(self, ware_key: str):
        """Set warehouse key."""
        self.ware_key = ware_key
        return self

    def set_cost(self, cost: float):
        """Set item cost."""
        self.cost = cost
        return self

    def set_weight(self, weight: int):
        """Set item weight."""
        self.weight = weight
        return self

    def set_amount(self, amount: int):
        """Set item amount."""
        self.amount = amount
        return self

    def set_brand(self, brand: str):
        """Set item brand."""
        self.brand = brand
        return self

    def set_country_code(self, country_code: str):
        """Set item country code."""
        self.country_code = country_code
        return self
