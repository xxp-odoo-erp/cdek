from dataclasses import dataclass
from .source import Source
from ..mixin.intakes import IntakesMixin
from ..mixin.common import CommonMixin
from ..mixin.package import PackageMixin

@dataclass
class Intakes(Source, IntakesMixin, CommonMixin, PackageMixin):
    """Класс для заявки на вызов курьера"""
