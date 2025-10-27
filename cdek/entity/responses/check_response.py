from dataclasses import dataclass
from .source import Source

from ...mixin.common import Common

@dataclass
class CheckResponse(Source, Common):
    date: str | None = None
    fiscal_storage_number: str | None = None
    document_number: str | None = None
    fiscal_sign: str | None = None
    type: str | None = None
    payment_info: list | None = None
