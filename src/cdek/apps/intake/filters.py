from __future__ import annotations

from datetime import date as Date
from uuid import UUID

from pydantic import BaseModel, Field, field_serializer

from ..models.location import Coordinates, Region, Zip


class IntakeStatus(BaseModel):
    code: str = Field(..., description="Код статуса")
    add_status: str = Field(..., description="Дополнительный код статуса")


class IntakeFilter(BaseModel):
    """Фильтр для заявок на вызов курьера"""

    uuid: UUID = Field(..., description="Идентификатор заявки в ИС СДЭК")
    status: IntakeStatus = Field(..., description="Статус заявки")


class IntakeLocation(Region, Coordinates, Zip):
    code: int | None = Field(default=None, description="Код населенного пункта СДЭК")
    city: str | None = Field(default=None, description="Название населенного пункта")
    fias_guid: UUID | None = Field(
        None, description="Уникальный идентификатор ФИАС населенного пункта"
    )
    address: str | None = Field(default=None, description="Строка адреса")
    region: str | None = Field(default=None, description="Название региона")  # type: ignore
    city_uuid: str | None = Field(
        default=None, description="Уникальный идентификатор населенного пункта"
    )


class IntakeDateFilter(BaseModel):
    from_location: IntakeLocation = Field(..., description="Адрес отправления")
    date: Date = Field(
        ..., description="До какого числа включительно получить доступные дни"
    )

    @field_serializer("date")
    def serialize_date(self, date: Date) -> str:
        """Представить дату фильтра в формате YYYY-MM-DD"""
        return date.strftime("%Y-%m-%d")
