from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, Field


class Error(BaseModel):
    """Ошибки"""

    code: Optional[str] = Field(None, description="Код ошибки")
    additional_code: Optional[str] = Field(
        None, description="Дополнительный код ошибки для службы поддержки"
    )
    message: Optional[str] = Field(None, description="Описание ошибки")
