from dataclasses import dataclass

from .source import Source

@dataclass
class RequestResponse(Source):
    request_uuid: str | None = None
    type: str | None = None
    date_time: str | None = None
    state: str | None = None
    errors: list | None = None
    warnings: list | None = None
