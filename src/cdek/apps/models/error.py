from __future__ import annotations

from pydantic import BaseModel, Field


class Error(BaseModel):
    """Ошибки"""

    code: str | None = Field(None, description="Код ошибки")
    additional_code: str | None = Field(
        None, description="Дополнительный код ошибки для службы поддержки"
    )
    message: str | None = Field(None, description="Описание ошибки")
