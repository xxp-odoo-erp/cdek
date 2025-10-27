from dataclasses import dataclass
from ...mixin.agreement import Agreement as AgreementMixin
from ...mixin.common import Common as CommonMixin
from .source import Source


@dataclass
class Agreement(Source, AgreementMixin, CommonMixin):
    """Договоренности о доставке"""
