from __future__ import annotations

from typing import Optional

from datetime import date as Date
from datetime import datetime
from uuid import UUID

from pydantic import Field, field_serializer

from ..models import Address, City, Coordinates, Country, Region, Zip
from ..models.order import OrderInfo
from ..request import BaseRequest


class ScheduleLocation(City, Country, Region, Coordinates, Address, Zip):
    code: Optional[int] = None
    region: Optional[str] = None
    region_code: Optional[int] = None
    city: Optional[str] = None
    city_uuid: Optional[str] = None


class DeliveryLocation(Zip, Coordinates, Country, Region):
    code: Optional[int] = None
    fias_guid: Optional[UUID] = None
    city: Optional[str] = None
    address: str


class RegisterDeliveryRequest(OrderInfo, BaseRequest):
    date: Date = Field(..., description="Дата доставки, согласованная с получателем")
    time_from: str = Field(
        ..., description='Время доставки "С", согласованное с получателем'
    )
    time_to: str = Field(
        ..., description='Время доставки "По", согласованное с получателем'
    )
    comment: Optional[str] = Field(
        None, max_length=255, description="Комментарий к договоренности о доставке"
    )
    delivery_point: Optional[str] = Field(
        None, max_length=255, description="Буквенно-цифровой код ПВЗ СДЭК"
    )
    to_location: Optional[ScheduleLocation] = Field(None, description="Населённый пункт")

    def to_location_init(self, **kwargs):
        """Создать объект локации для договорённости о доставке"""
        return ScheduleLocation(**kwargs)

    def set_to_location(self, location: ScheduleLocation):
        """Установить локацию доставки"""
        self.to_location = location
        return self

    @field_serializer("date")
    def serialize_date(self, date: Date) -> str:
        """Вернуть дату доставки в формате YYYY-MM-DD"""
        return date.strftime("%Y-%m-%d")


class DeliveryIntervalRequest(BaseRequest):
    date_time: datetime = Field(..., description="Дата и время заявки на вызов курьера")
    from_location: Optional[DeliveryLocation] = Field(
        None, description="Адрес отправления"
    )
    shipment_point: Optional[str] = Field(None, description="Код ПВЗ СДЭК")
    to_location: DeliveryLocation = Field(..., description="Адрес доставки")
    tariff_code: int = Field(..., description="Код тарифа")
    additional_order_types: Optional[list[int]] = Field(
        None, description="Дополнительные типы заказа"
    )

    @field_serializer("date_time")
    def serialize_date_time(self, date_time: datetime) -> str:
        """Вернуть дату запроса интервалов в формате ISO 8601"""
        return date_time.strftime("%Y-%m-%dT%H:%M:%S")
