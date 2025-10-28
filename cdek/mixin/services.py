from dataclasses import dataclass

@dataclass
class ServicesMixin:
    """Mixin for additional services."""
    
    code: str | None = None
    parameter: float | None = None
