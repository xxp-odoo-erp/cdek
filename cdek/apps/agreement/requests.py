from datetime import date as Date
from datetime import datetime
from uuid import UUID

from pydantic import Field, field_serializer

from ..models import Address, City, Coordinates, Country, Region, Zip
from ..models.order import OrderInfo
from ..request import BaseRequest


class ScheduleLocation(City, Country, Region, Coordinates, Address, Zip):
    code: int | None = None
    region: str | None = None
    region_code: int | None = None
    city: str | None = None
    city_uuid: str | None = None


class DeliveryLocation(Zip, Coordinates, Country, Region):
    code: int | None = None
    fias_guid: UUID | None = None
    city: str | None = None
    address: str


class RegisterDeliveryRequest(OrderInfo, BaseRequest):
    date: Date = Field(..., description="Дата доставки, согласованная с получателем")
    time_from: str = Field(
        ..., description='Время доставки "С", согласованное с получателем'
    )
    time_to: str = Field(
        ..., description='Время доставки "По", согласованное с получателем'
    )
    comment: str | None = Field(
        None, max_length=255, description="Комментарий к договоренности о доставке"
    )
    delivery_point: str | None = Field(
        None, max_length=255, description="Буквенно-цифровой код ПВЗ СДЭК"
    )
    to_location: ScheduleLocation | None = Field(None, description="Населённый пункт")

    def to_location_init(self, **kwargs):
        return ScheduleLocation(**kwargs)

    def set_to_location(self, location: ScheduleLocation):
        self.to_location = location
        return self

    @field_serializer("date")
    def serialize_date(self, date: Date) -> str:
        return date.strftime("%Y-%m-%d")


class DeliveryIntervalRequest(BaseRequest):
    date_time: datetime = Field(..., description="Дата и время заявки на вызов курьера")
    from_location: DeliveryLocation | None = Field(
        None, description="Адрес отправления"
    )
    shipment_point: str | None = Field(None, description="Код ПВЗ СДЭК")
    to_location: DeliveryLocation = Field(..., description="Адрес доставки")
    tariff_code: int = Field(..., description="Код тарифа")
    additional_order_types: list[int] | None = Field(
        None, description="Дополнительные типы заказа"
    )

    @field_serializer("date_time")
    def serialize_date_time(self, date_time: datetime) -> str:
        return date_time.strftime("%Y-%m-%dT%H:%M:%S")
