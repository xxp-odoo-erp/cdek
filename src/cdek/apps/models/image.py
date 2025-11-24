from __future__ import annotations

from pydantic import BaseModel, Field


class Image(BaseModel):
    number: int | None = Field(0, description="Номер фото")
    url: str = Field(..., max_length=255, description="Ссылка на фото")
