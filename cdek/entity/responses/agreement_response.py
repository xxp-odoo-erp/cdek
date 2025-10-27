from dataclasses import dataclass, field

from .source import Source
from ...mixin.common import Common as CommonMixin
from ...mixin.agreement import Agreement as AgreementMixin
from .statuses_response import StatusesResponse

@dataclass
class AgreementResponse(Source, CommonMixin, AgreementMixin):

    statuses: list[StatusesResponse] = field(default_factory=list)

    def get_statuses(self):
        return self.statuses
