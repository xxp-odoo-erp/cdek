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
    code: int | None = Field(None, description="Код населенного пункта СДЭК")
    city: str | None = Field(None, description="Название населенного пункта")
    fias_guid: UUID | None = Field(None, description="Уникальный идентификатор ФИАС населенного пункта")
    address: str | None = Field(None, description="Строка адреса")
    region: str | None = Field(None, description="Название региона")
    city_uuid: str | None = Field(None, description="Уникальный идентификатор населенного пункта")


class IntakeDateFilter(BaseRequest):
    from_location: IntakeLocation = Field(..., description="Адрес отправления")
    date: Date = Field(..., description="До какого числа включительно получить доступные дни")

    @field_serializer("date")
    def serialize_date(self, date: Date) -> str:
        return date.strftime("%Y-%m-%d")