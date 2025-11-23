"""Модель для работы с телефоном."""

from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, Field


class Phone(BaseModel):
    """Модель для телефонного номера."""

    number: str = Field(..., max_length=24, description="Номер телефона")
    additional: Optional[str] = Field(
        None, max_length=255, description="Дополнительная информация (добавочный номер)"
    )
