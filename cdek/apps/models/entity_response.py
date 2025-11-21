from __future__ import annotations

from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field

from .related_entity import RelatedEntity
from .request import Request


class RootEntity(BaseModel):
    uuid: UUID = Field(..., description="Идентификатор сущности в ИС СДЭК")


class EntityResponse(BaseModel):
    """Модель ответа о сущности."""

    entity: Optional[RootEntity] = Field(
        default=None, description="Идентификатор сущности в ИС СДЭК"
    )
    requests: Optional[list[Request]] = None
    related_entities: Optional[list[RelatedEntity]] = None

    def get_entry_uuid(self) -> Optional[str]:
        """Получить UUID сущности."""
        if self.entity is None:
            return None
        if hasattr(self.entity, "uuid"):
            return str(self.entity.uuid)
        return None

    def get_entity(self) -> Optional[RootEntity]:
        """Получить данные сущности."""
        if self.entity is None:
            return None
        return self.entity

    def get_requests(self) -> list[Request]:
        """Получить список запросов."""
        if self.requests is None:
            return []
        return self.requests
