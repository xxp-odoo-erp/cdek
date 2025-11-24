from __future__ import annotations

from enum import Enum

from pydantic import BaseModel, Field


class PrintType(str, Enum):
    """Типы печатной формы"""

    tpl_china = "tpl_china"
    tpl_armenia = "tpl_armenia"
    tpl_russia = "tpl_russia"
    tpl_english = "tpl_english"
    tpl_italian = "tpl_italian"
    tpl_korean = "tpl_korean"
    tpl_latvian = "tpl_latvian"
    tpl_lithuanian = "tpl_lithuanian"
    tpl_german = "tpl_german"
    tpl_turkish = "tpl_turkish"
    tpl_czech = "tpl_czech"
    tpl_thailand = "tpl_thailand"
    tpl_invoice = "tpl_invoice"


class PrintOrder(BaseModel):
    order_uuid: str | None = Field(None, description="Идентификатор заказа в ИС СДЭК")
    cdek_number: int | None = Field(None, description="Номер заказа СДЭК")


class PrintForm(BaseModel):
    orders: list[PrintOrder] = Field(..., description="Список заказов")
    copy_count: int | None = Field(None, description="Количество копий")
