from dataclasses import dataclass
from .source import Source

@dataclass
class Webhooks(Source):
    """Класс для webhooks"""

    type: str | None = None
    url: str | None = None

    def set_type(self, webhook_type: str):
        """Установить тип события"""
        self.type = webhook_type
        return self

    def set_url(self, url: str):
        """Установить URL"""
        self.url = url
        return self

