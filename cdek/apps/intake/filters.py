from __future__ import annotations

from typing import Optional

from datetime import date as Date
from uuid import UUID

from pydantic import Field, field_serializer

from ..models.location import Coordinates, Region, Zip
from ..request import BaseRequest


class IntakeStatus(BaseRequest):
    code: str = Field(..., description="Код статуса")
    add_status: str = Field(..., description="Дополнительный код статуса")


class IntakeFilter(BaseRequest):
    """Фильтр для заявок на вызов курьера"""

    uuid: UUID = Field(..., description="Идентификатор заявки в ИС СДЭК")
    status: IntakeStatus = Field(..., description="Статус заявки")


class IntakeLocation(BaseRequest, Region, Coordinates, Zip):
    code: Optional[int] = Field(None, description="Код населенного пункта СДЭК")
    city: Optional[str] = Field(None, description="Название населенного пункта")
    fias_guid: Optional[UUID] = Field(
        None, description="Уникальный идентификатор ФИАС населенного пункта"
    )
    address: Optional[str] = Field(None, description="Строка адреса")
    region: Optional[str] = Field(None, description="Название региона")
    city_uuid: Optional[str] = Field(
        None, description="Уникальный идентификатор населенного пункта"
    )


class IntakeDateFilter(BaseRequest):
    from_location: IntakeLocation = Field(..., description="Адрес отправления")
    date: Date = Field(
        ..., description="До какого числа включительно получить доступные дни"
    )

    @field_serializer("date")
    def serialize_date(self, date: Date) -> str:
        """Представить дату фильтра в формате YYYY-MM-DD"""
        return date.strftime("%Y-%m-%d")
