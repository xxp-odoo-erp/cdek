from dataclasses import dataclass
from .express import Express

@dataclass
class Phone(Express):
    number: str | None = None
    additional: str | None = None
