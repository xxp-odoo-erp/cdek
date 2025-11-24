from __future__ import annotations

from datetime import date as Date

from pydantic import BaseModel, Field, field_serializer


class CheckFilter(BaseModel):
    """Фильтр для получения информации о чеке"""

    order_uuid: str | None = Field(..., description="Идентификатор заказа")
    cdek_number: str | None = Field(..., description="Номер заказа СДЭК")
    date: Date | None = Field(
        ..., description="Дата создания чека в формате YYYY-MM-DD"
    )

    @field_serializer("date")
    def serialize_date(self, date: Date) -> str:
        """Преобразовать дату фильтра в строку YYYY-MM-DD"""
        return date.strftime("%Y-%m-%d")
