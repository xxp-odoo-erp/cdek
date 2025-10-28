from dataclasses import dataclass
from ..mixin.agreement import AgreementMixin
from ..mixin.common import CommonMixin
from .source import Source


@dataclass
class Agreement(Source, AgreementMixin, CommonMixin):
    """Договоренности о доставке"""
