from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..entity.requests.contact import Contact
    from ..entity.requests.money import Money
    from ..entity.requests.seller import Seller
    from ..entity.requests.threshold import Threshold

@dataclass
class Order:
    number: str | None = None
    developer_key: str | None = None
    shipment_point: str | None = None
    delivery_point: str | None = None
    items_cost_currency: str | None = None
    recipient_currency: str | None = None
    shipper_name: str | None = None
    shipper_address: str | None = None
    delivery_recipient_cost: 'Money | None' = None
    delivery_recipient_cost_adv: 'list[Threshold] | None' = None
    seller: 'Seller | None' = None
    recipient: 'Contact | None' = None

    def set_shipment_point(self, shipment_point: str):
        self.shipment_point = shipment_point
        return self

    def set_delivery_point(self, delivery_point: str):
        self.delivery_point = delivery_point
        return self
