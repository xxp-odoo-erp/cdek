from dataclasses import dataclass
from .source import Source


@dataclass
class CallsResponse(Source):

    failed_calls: list | None = None
    reason_code: str | None = None
    date_time: str | None = None
    rescheduled_calls: list | None = None
