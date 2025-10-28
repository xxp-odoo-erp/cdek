from dataclasses import dataclass
from .source import Source

@dataclass
class StatusesResponse(Source):

    code: str | None = None
    name: str | None = None
    reason_code: str | None = None
    date_time: str | None = None
    city: str | None = None
    deleted: bool | None = None
