from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, Field


class WarningModel(BaseModel):
    """Предупреждения"""

    code: Optional[str] = Field(None, description="Код предупреждения")
    message: Optional[str] = Field(None, description="Описание предупреждения")
