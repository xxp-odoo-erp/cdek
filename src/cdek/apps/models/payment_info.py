from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field


class PaymentInfo(BaseModel):
    sum: float = Field(..., description="Сумма платежа")
    type: Literal["CASH", "CARD"] = Field(..., description="Тип платежа")
