from __future__ import annotations

from datetime import date as Date
from datetime import datetime
from enum import Enum
from uuid import UUID

from pydantic import BaseModel, Field, field_serializer, field_validator


class RelatedEntityType(str, Enum):
    """Типы связанных сущностей"""

    RETURN_ORDER = "RETURN_ORDER"
    DIRECT_ORDER = "DIRECT_ORDER"
    CLIENT_RETURN_ORDER = "CLIENT_RETURN_ORDER"
    CLIENT_DIRECT_ORDER = "CLIENT_DIRECT_ORDER"
    WAYBILL = "WAYBILL"
    BARCODE = "BARCODE"
    REVERSE_ORDER = "REVERSE_ORDER"
    DELIVERY = "DELIVERY"


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

    @field_validator("type", mode="before")
    @classmethod
    def convert_type_to_upper(cls, v: str) -> str:
        """Преобразование типа в верхний регистр перед валидацией"""
        return isinstance(v, str) and v.upper() or v

    @field_serializer("create_time")
    def serialize_create_time(self, create_time: datetime) -> str:
        """Конвертировать время создания в строку ISO"""
        return create_time.strftime("%Y-%m-%dT%H:%M:%S")

    @field_serializer("date")
    def serialize_date(self, date: Date) -> str:
        """Конвертировать дату доставки в формат YYYY-MM-DD"""
        return date.strftime("%Y-%m-%d")
