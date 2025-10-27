"""
Класс IntakesResponse для ответов от API
"""

from .source import Source
from ...mixin.intakes import Intakes as IntakesMixin
from ...mixin.common import Common as CommonMixin
from ...mixin.package import Package as PackageMixin
from .statuses_response import StatusesResponse

class IntakesResponse(IntakesMixin, CommonMixin, PackageMixin, Source):

    intake_number: str | None = None
    statuses: list[StatusesResponse] | None = None
