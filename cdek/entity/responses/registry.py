from dataclasses import dataclass, field
from .source import Source


@dataclass
class RegistryResponse(Source):
    """Класс для ответа о реестре"""
    registries: list | None = field(default_factory=list)

    def __init__(self, properties=None):
        """Переопределяем __init__ чтобы вызвать родительский"""
        Source.__init__(self, properties)
