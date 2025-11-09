from datetime import date as Date
from datetime import datetime
from enum import StrEnum, auto
from uuid import UUID

from pydantic import BaseModel, Field, field_serializer


class RelatedEntityType(StrEnum):
    """Типы связанных сущностей"""

    RETURN_ORDER = auto()
    DIRECT_ORDER = auto()
    CLIENT_RETURN_ORDER = auto()
    CLIENT_DIRECT_ORDER = auto()
    WAYBILL = auto()
    BARCODE = auto()
    REVERSE_ORDER = auto()
    DELIVERY = auto()


class RelatedEntity(BaseModel):
    """Связанные сущности"""

    uuid: UUID | None = Field(None, description="Идентификатор сущности в ИС СДЭК")
    type: RelatedEntityType = Field(..., description="Тип связанной сущности")
    url: str | None = Field(
        None, max_length=255, description="Ссылка на скачивание печатной формы"
    )
    create_time: datetime | None = Field(
        None, description="Время создания связанной сущности"
    )
    cdek_number: str | None = Field(
        None, max_length=255, description="Номер заказа СДЭК"
    )
    date: Date | None = Field(
        None, description="Дата доставки, согласованная с получателем"
    )
    time_from: str | None = Field(None, description="Время начала ожидания курьера")
    time_to: str | None = Field(None, description="Время окончания ожидания курьера")

    @field_serializer("create_time")
    def serialize_create_time(self, create_time: datetime) -> str:
        return create_time.strftime("%Y-%m-%dT%H:%M:%S")

    @field_serializer("date")
    def serialize_date(self, date: Date) -> str:
        return date.strftime("%Y-%m-%d")
