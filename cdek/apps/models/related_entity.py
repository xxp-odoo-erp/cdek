from __future__ import annotations

from typing import Optional

from datetime import date as Date
from datetime import datetime
from enum import Enum
from uuid import UUID

from pydantic import BaseModel, Field, field_serializer


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

    uuid: Optional[UUID] = Field(None, description="Идентификатор сущности в ИС СДЭК")
    type: RelatedEntityType = Field(..., description="Тип связанной сущности")
    url: Optional[str] = Field(
        None, max_length=255, description="Ссылка на скачивание печатной формы"
    )
    create_time: Optional[datetime] = Field(
        None, description="Время создания связанной сущности"
    )
    cdek_number: Optional[str] = Field(
        None, max_length=255, description="Номер заказа СДЭК"
    )
    date: Optional[Date] = Field(
        None, description="Дата доставки, согласованная с получателем"
    )
    time_from: Optional[str] = Field(None, description="Время начала ожидания курьера")
    time_to: Optional[str] = Field(None, description="Время окончания ожидания курьера")

    @field_serializer("create_time")
    def serialize_create_time(self, create_time: datetime) -> str:
        """Конвертировать время создания в строку ISO"""
        return create_time.strftime("%Y-%m-%dT%H:%M:%S")

    @field_serializer("date")
    def serialize_date(self, date: Date) -> str:
        """Конвертировать дату доставки в формат YYYY-MM-DD"""
        return date.strftime("%Y-%m-%d")
