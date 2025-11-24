from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field, field_serializer


class Status(BaseModel):
    code: str = Field(..., description="Код статуса")
    name: str = Field(..., description="Название статуса")
    date_time: datetime = Field(..., description="Дата и время статуса")

    @field_serializer("date_time")
    def serialize_date_time(self, date_time: datetime) -> str:
        """Преобразовать дату статуса в строку формата ISO"""
        return date_time.strftime("%Y-%m-%dT%H:%M:%S")
