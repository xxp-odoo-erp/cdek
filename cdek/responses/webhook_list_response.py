from .source import Source
from dataclasses import dataclass

@dataclass
class WebhookListResponse(Source):
    """Класс для ответа о webhooklist"""

    type: str | None = None
    uuid: str | None = None
    url: str | None = None
