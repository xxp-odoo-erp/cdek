from __future__ import annotations

from pydantic import BaseModel, Field


class Vat(BaseModel):
    vat_sum: float | None = Field(None, description="Сумма НДС")
    vat_rate: int | None = Field(None, description="Ставка НДС")


class Money(Vat):
    """Модель для денежных сумм и НДС."""

    value: float | None = Field(None, description="Сумма платежа, включая НДС")
