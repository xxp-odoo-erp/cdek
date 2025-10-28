from dataclasses import dataclass
from .source import Source
from ..mixin.delivery_points import DeliveryPointsMixin

@dataclass
class DeliveryPointsResponse(Source, DeliveryPointsMixin):
    name: str | None = None
    code: str | None = None
    location: list | None = None
    work_time: str | None = None
    work_time_list: list | None = None
    work_time_exceptions: list | None = None
    note: str | None = None
    owner_code: str | None = None
    nearest_station: str | None = None
    nearest_metro_station: str | None = None
    site: str | None = None
    email: str | None = None
    address_comment: str | None = None
    office_image_list: list | None = None
    dimensions: list | None = None
    fulfillment: bool | None = None
    phones: list | None = None
    type: str | None = None
