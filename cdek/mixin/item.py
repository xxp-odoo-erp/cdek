from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..entity.requests.money import Money

@dataclass
class Item:
    name: str | None = None
    ware_key: str | None = None
    marking: str | None = None
    payment: 'Money | None' = None
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
        from ..entity.requests.money import Money
        self.payment = Money.express({'value': value, 'vat_sum': vat_sum or 0, 'vat_rate': vat_rate or 20})
        return self

    def set_name(self, name: str):
        self.name = name
        return self

    def set_ware_key(self, ware_key: str):
        self.ware_key = ware_key
        return self

    def set_cost(self, cost: float):
        self.cost = cost
        return self

    def set_weight(self, weight: int):
        self.weight = weight
        return self

    def set_amount(self, amount: int):
        self.amount = amount
        return self

    def set_brand(self, brand: str):
        self.brand = brand
        return self

    def set_country_code(self, country_code: str):
        self.country_code = country_code
        return self
