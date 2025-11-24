from __future__ import annotations

from datetime import datetime as DateTime
from typing import Literal

from pydantic import BaseModel, Field, field_serializer

from ..models.error import Error
from ..models.payment_info import PaymentInfo
from ..models.warning import WarningModel


class CheckInfo(BaseModel):
    order_uuid: str = Field(..., description="Идентификатор заказа")
    cdek_number: str = Field(..., description="Номер заказа СДЭК")
    date: DateTime = Field(..., description="Дата создания чека в формате YYYY-MM-DD")
    document_number: str = Field(..., description="Номер документа")
    fiscal_sign: int = Field(..., description="Фискальный признак")
    type: Literal["CASH_RECEIPT_IN", "CASH_RECEIPT_REFUND"] = Field(
        ..., description="Тип чека"
    )
    payment_info: list[PaymentInfo] = Field(..., description="Информация о платеже")
    shift_no: int | None = Field(None, description="Номер смены")

    @field_serializer("date")
    def serialize_date(self, date: DateTime) -> str:
        """Вернуть дату формирования чека в формате YYYY-MM-DD"""
        return date.strftime("%Y-%m-%d")


class CheckResponse(BaseModel):
    check_info: list[CheckInfo] = Field(..., description="Информация о чеке")
    errors: list[Error] | None = Field(None, description="Список ошибок")
    warnings: list[WarningModel] | None = Field(
        None, description="Список предупреждений"
    )
