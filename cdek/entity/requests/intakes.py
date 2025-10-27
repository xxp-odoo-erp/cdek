from dataclasses import dataclass
from .source import Source
from ...mixin.intakes import Intakes as IntakesMixin
from ...mixin.common import Common as CommonMixin
from ...mixin.package import Package as PackageMixin

@dataclass
class Intakes(Source, IntakesMixin, CommonMixin, PackageMixin):
    """Класс для заявки на вызов курьера"""
