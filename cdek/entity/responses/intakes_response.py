"""
Класс IntakesResponse для ответов от API
"""

from dataclasses import dataclass, field
from .source import Source
from ...mixin.intakes import Intakes as IntakesMixin
from ...mixin.common import Common as CommonMixin
from ...mixin.package import Package as PackageMixin
from .statuses_response import StatusesResponse

@dataclass
class IntakesResponse(IntakesMixin, CommonMixin, PackageMixin, Source):

    intake_number: str | None = None
    statuses: list[StatusesResponse] | None = None
    packages: list | None = field(default=None)
    to_location: dict | None = None  # Дополнительное поле от API для локации доставки
    contragent_uuid: str | None = None  # Дополнительное поле от API для UUID контрагента
    requests: list | None = field(default=None)  # Дополнительное поле от API для запросов
