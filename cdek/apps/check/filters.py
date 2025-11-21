from __future__ import annotations

from typing import Optional

from datetime import date as Date

from pydantic import Field, field_serializer

from ..request import BaseRequest


class CheckFilter(BaseRequest):
    """Фильтр для получения информации о чеке"""

    order_uuid: Optional[str] = Field(..., description="Идентификатор заказа")
    cdek_number: Optional[str] = Field(..., description="Номер заказа СДЭК")
    date: Optional[Date] = Field(
        ..., description="Дата создания чека в формате YYYY-MM-DD"
    )

    @field_serializer("date")
    def serialize_date(self, date: Date) -> str:
        """Преобразовать дату фильтра в строку YYYY-MM-DD"""
        return date.strftime("%Y-%m-%d")
