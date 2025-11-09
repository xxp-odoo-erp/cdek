from uuid import UUID

from pydantic import BaseModel, Field

from .related_entity import RelatedEntity
from .request import Request


class RootEntity(BaseModel):
    uuid: UUID = Field(..., description="Идентификатор сущности в ИС СДЭК")


class EntityResponse(BaseModel):
    """Модель ответа о сущности."""

    requests: list[Request] | None = None
    entity: RootEntity | None = Field(default=None, description="Идентификатор сущности в ИС СДЭК")
    uuid: str | None = None
    related_entities: list[RelatedEntity] | None = None

    def get_entry_uuid(self) -> str | None:
        """Получить UUID сущности."""
        if hasattr(self, "uuid") and self.uuid:
            return str(self.uuid) if isinstance(self.uuid, UUID) else self.uuid
        if self.entity is not None:
            if isinstance(self.entity, RootEntity):
                return str(self.entity.uuid)
            elif isinstance(self.entity, dict):
                uuid_value = self.entity.get("uuid")
                return str(uuid_value) if isinstance(uuid_value, UUID) else uuid_value
            elif isinstance(self.entity, list) and len(self.entity) > 0:
                first_entity = self.entity[0]
                if isinstance(first_entity, RootEntity):
                    return str(first_entity.uuid)
                elif isinstance(first_entity, dict):
                    uuid_value = first_entity.get("uuid")
                    return str(uuid_value) if isinstance(uuid_value, UUID) else uuid_value
        return None

    def get_entity(self) -> RootEntity | None:
        """Получить данные сущности."""
        if self.entity is None:
            return None
        return self.entity

    def get_requests(self) -> list[Request]:
        """Получить список запросов."""
        if self.requests is None:
            return []
        return self.requests
