from dataclasses import dataclass, field

from .source import Source
from ..requests.delivery_mode import DeliveryMode


@dataclass
class TariffEntryResponse(Source):

    tariff_name: str | None = None
    weight_min: float | None = None
    weight_max: float | None = None
    weight_calc_max: float | None = None
    length_min: float | None = None
    length_max: float | None = None
    width_min: float | None = None
    width_max: float | None = None
    height_min: float | None = None
    height_max: float | None = None
    order_types: list[str] | None = None
    payer_contragent_type: list[str] | None = None
    sender_contragent_type: list[str] | None = None
    recipient_contragent_type: list[str] | None = None
    delivery_modes: list[DeliveryMode] | None = None
    additional_order_types_param: dict | None = None
