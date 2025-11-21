from __future__ import annotations

from datetime import date as Date
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field, field_serializer

from .contact import Contact
from .location import Address, City, Coordinates, Country, Region, Zip


class IntakeLocation(City, Country, Region, Coordinates, Zip, Address):
    address: str = Field(..., description="Строка адреса")
    region: Optional[str] = Field(None, description="Название региона")
    city: Optional[str] = Field(None, description="Название населенного пункта")
    city_uuid: Optional[str] = Field(
        None, description="Уникальный идентификатор населенного пункта"
    )


class Intakes(BaseModel):
    cdek_number: Optional[str] = Field(None, description="Номер заказа СДЭК")
    order_uuid: Optional[UUID] = Field(None, description="Идентификатор заказа")
    intake_date: Date = Field(..., description="Дата заявки на вызов курьера")
    intake_time_from: str = Field(
        ..., description="Время начала заявки на вызов курьера"
    )
    intake_time_to: str = Field(
        ..., description="Время окончания заявки на вызов курьера"
    )
    lunch_time_from: str = Field(..., description="Время начала обеда")
    lunch_time_to: str = Field(..., description="Время окончания обеда")
    name: Optional[str] = Field(None, description="Имя заказчика")
    weight: Optional[int] = Field(None, description="Вес заявки")
    length: Optional[int] = Field(None, description="Длина заявки")
    width: Optional[int] = Field(None, description="Ширина заявки")
    height: Optional[int] = Field(None, description="Высота заявки")
    comment: Optional[str] = Field(None, description="Комментарий к заявке")
    courier_power_of_attorney: Optional[bool] = Field(
        None, description="Нужно ли вызывать курьера"
    )
    courier_identity_card: Optional[bool] = Field(
        None, description="Нужно ли вызывать курьера"
    )
    sender: Optional[Contact] = Field(None, description="Контакт заказчика")
    from_location: Optional[IntakeLocation] = Field(None, description="Населённый пункт")
    need_call: bool = Field(False, description="Необходим прозвон получателя")

    @field_serializer("intake_date")
    def serialize_intake_date(self, intake_date: Date) -> str:
        """Представить дату забора в формате YYYY-MM-DD"""
        return intake_date.strftime("%Y-%m-%d")

    def from_location_init(self, **kwargs):
        """Создать объект адреса забора по переданным параметрам"""
        return IntakeLocation(**kwargs)

    def sender_init(self, **kwargs):
        """Создать объект контакта заказчика"""
        return Contact(**kwargs)

    def set_sender(self, sender: Contact):
        """Установить контактные данные заказчика"""
        self.sender = sender
        return self

    def set_from_location(self, location: IntakeLocation):
        """Указать место забора"""
        self.from_location = location
        return self
