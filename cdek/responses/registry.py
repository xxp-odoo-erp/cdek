from dataclasses import dataclass, field
from .source import Source


@dataclass
class RegistryResponse(Source):
    """Класс для ответа о реестре"""
    registries: list | None = field(default_factory=list)
