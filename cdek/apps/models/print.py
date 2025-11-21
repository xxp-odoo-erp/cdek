from enum import StrEnum, auto

from pydantic import BaseModel, Field


class PrintType(StrEnum):
    """Типы печатной формы"""

    tpl_china = auto()
    tpl_armenia = auto()
    tpl_russia = auto()
    tpl_english = auto()
    tpl_italian = auto()
    tpl_korean = auto()
    tpl_latvian = auto()
    tpl_lithuanian = auto()
    tpl_german = auto()
    tpl_turkish = auto()
    tpl_czech = auto()
    tpl_thailand = auto()
    tpl_invoice = auto()


class PrintOrder(BaseModel):
    order_uuid: str | None = Field(None, description="Идентификатор заказа в ИС СДЭК")
    cdek_number: int | None = Field(None, description="Номер заказа СДЭК")


class PrintForm(BaseModel):
    orders: list[PrintOrder] = Field(..., description="Список заказов")
    copy_count: int | None = Field(None, description="Количество копий")
