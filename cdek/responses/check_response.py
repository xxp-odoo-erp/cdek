from dataclasses import dataclass
from .source import Source

from ..mixin.common import CommonMixin

@dataclass
class CheckResponse(Source, CommonMixin):
    date: str | None = None
    fiscal_storage_number: str | None = None
    document_number: str | None = None
    fiscal_sign: str | None = None
    type: str | None = None
    payment_info: list | None = None
