from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, Field


class Vat(BaseModel):
    vat_sum: Optional[float] = Field(None, description="Сумма НДС")
    vat_rate: Optional[int] = Field(None, description="Ставка НДС")


class Money(Vat):
    """Модель для денежных сумм и НДС."""

    value: Optional[float] = Field(None, description="Сумма платежа, включая НДС")

    @classmethod
    def init(cls, **kwargs):
        """Экспресс-метод создания Money."""
        return cls(**kwargs)
