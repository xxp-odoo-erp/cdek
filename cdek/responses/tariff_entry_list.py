from dataclasses import dataclass, field

from .source import Source
from .tariff_entry import TariffEntryResponse

@dataclass
class TariffEntryListResponse(Source):
    """Класс для ответа от API с информацией о тарифе"""

    tariff_codes: list[TariffEntryResponse] | None = field(default_factory=list)