from dataclasses import dataclass
from .invoice import Invoice


@dataclass
class Barcode(Invoice):
    """Класс для ШК-места"""

    format: str | None = None
    lang: str | None = None

    def set_format(self, format: str = 'A4'):
        """Установить формат печати"""
        self.format = format
        return self

    def set_lang(self, lang: str):
        """Установить язык"""
        self.lang = lang
        return self
