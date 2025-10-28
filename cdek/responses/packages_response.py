from .source import Source
from ..mixin.package import PackageMixin
from dataclasses import dataclass

@dataclass
class PackagesResponse(Source, PackageMixin):
    """Класс для ответа о packages"""

    package_id: str | None = None
    weight_volume: int | None = None
    weight_calc: int | None = None

    def get_weight_volume(self) -> int | None:
        return self.weight_volume

    def get_weight_calc(self) -> int | None:
        return self.weight_calc

    def get_package_id(self) -> str | None:
        return self.package_id
