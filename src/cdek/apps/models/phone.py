"""Модель для работы с телефоном."""

from __future__ import annotations

from pydantic import BaseModel, Field


class Phone(BaseModel):
    """Модель для телефонного номера."""

    number: str = Field(..., max_length=24, description="Номер телефона")
    additional: str | None = Field(
        None, max_length=255, description="Дополнительная информация (добавочный номер)"
    )
