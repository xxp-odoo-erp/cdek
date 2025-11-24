from __future__ import annotations

from pydantic import BaseModel, Field


class Dimensions(BaseModel):
    width: int = Field(..., description="Ширина (см)")
    height: int = Field(..., description="Высота (см)")
    depth: int = Field(..., description="Глубина (см)")
