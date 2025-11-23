from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, Field


class Image(BaseModel):
    number: Optional[int] = Field(0, description="Номер фото")
    url: str = Field(..., max_length=255, description="Ссылка на фото")
