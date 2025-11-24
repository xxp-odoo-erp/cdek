from __future__ import annotations

from pydantic import BaseModel, Field


class WarningModel(BaseModel):
    """Предупреждения"""

    code: str | None = Field(None, description="Код предупреждения")
    message: str | None = Field(None, description="Описание предупреждения")
