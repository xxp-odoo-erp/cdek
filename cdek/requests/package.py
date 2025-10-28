from dataclasses import dataclass
from .source import Source
from ..mixin.package import PackageMixin

@dataclass
class Package(Source, PackageMixin):
    """Класс для работы с упаковкой"""
