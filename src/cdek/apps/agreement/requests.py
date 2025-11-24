from __future__ import annotations

from datetime import date as Date
from datetime import datetime
from typing import Any
from uuid import UUID

from pydantic import BaseModel, Field, field_serializer

from ..models import Address, City, Coordinates, Country, Region, Zip
from ..models.order import OrderInfo


class ScheduleLocation(City, Country, Region, Coordinates, Address, Zip):
    code: int | None = Field(default=None)  # type: ignore
    region: str | None = Field(default=None)  # type: ignore
    region_code: int | None = Field(default=None)
    city: str | None = Field(default=None)  # type: ignore
    city_uuid: str | None = Field(default=None)  # type: ignore


class DeliveryLocation(Zip, Coordinates, Country, Region):
    code: int | None = None
    fias_guid: UUID | None = None
    city: str | None = None
    address: str


class RegisterDeliveryRequest(OrderInfo):
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

    def to_location_init(self, **kwargs: Any) -> ScheduleLocation:
        """Создать объект локации для договорённости о доставке"""
        return ScheduleLocation(**kwargs)

    def set_to_location(self, location: ScheduleLocation) -> RegisterDeliveryRequest:
        """Установить локацию доставки"""
        self.to_location = location
        return self

    @field_serializer("date")
    def serialize_date(self, date: Date) -> str:
        """Вернуть дату доставки в формате YYYY-MM-DD"""
        return date.strftime("%Y-%m-%d")


class DeliveryIntervalRequest(BaseModel):
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
        """Вернуть дату запроса интервалов в формате ISO 8601"""
        return date_time.strftime("%Y-%m-%dT%H:%M:%S")
