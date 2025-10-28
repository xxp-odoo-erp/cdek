from dataclasses import dataclass

from .source import Source
from .responses import RequestResponse


@dataclass
class EntityResponse(Source):
    requests: list[RequestResponse] | None = None
    entity: dict | None = None
    uuid: str | None = None
    related_entities: list | None = None

    def get_entry_uuid(self) -> str | None:
        # Сначала пытаемся получить из uuid
        if hasattr(self, 'uuid') and self.uuid:
            return self.uuid
        # Затем из entity
        if self.entity is not None:
            if isinstance(self.entity, dict):
                return self.entity.get('uuid')
            elif isinstance(self.entity, list) and len(self.entity) > 0:
                return self.entity[0].get('uuid') if isinstance(self.entity[0], dict) else None
        return None

    def get_entity(self) -> dict | list | None:
        if self.entity is None:
            return None
        return self.entity

    def get_requests(self) -> list[RequestResponse] | None:
        if self.requests is None:
            return None
        return self.requests
