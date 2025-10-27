from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..entity.requests.location import Location
    from ..entity.requests.package import Package
    from ..entity.requests.services import Services


@dataclass
class Tariff:
    type: int | None = None
    tariff_code: int | None = None
    from_location: 'Location | None' = None
    to_location: 'Location | None' = None
    services: 'list[Services] | None' = None
    packages: 'list[Package] | None' = None
    date: str | None = None
    currency: int | None = None

    def set_type(self, type: int):
        if type not in [1, 2]:
            raise ValueError("Invalid type")
        self.type = type
        return self

    def set_tariff_code(self, tariff_code: int):
        self.tariff_code = tariff_code
        return self

    def get_tariff_code(self):
        return self.tariff_code

    def add_service(self, service: 'Services'):
        if self.services is None:
            self.services = []
        self.services.append(service)
        return self

    def add_package(self, package: 'Package'):
        if self.packages is None:
            self.packages = []
        self.packages.append(package)
        return self

    def set_from_location(self, location: 'Location'):
        self.from_location = location
        return self

    def set_to_location(self, location: 'Location'):
        self.to_location = location
        return self

    def set_services(self, service: 'Services'):
        if self.services is None:
            self.services = []
        self.services.append(service)
        return self

    def set_packages(self, package: 'Package'):
        if self.packages is None:
            self.packages = []
        self.packages.append(package)
        return self

    def set_city_codes(self, from_code: int, to_code: int):
        """Установить коды городов отправления и назначения"""
        self.from_location = None
        self.to_location = None
        from ..entity.requests.location import Location
        self.from_location = Location(code=from_code)
        self.to_location = Location(code=to_code)
        return self

    def set_package_weight(self, weight: int):
        """Установить вес посылки в граммах"""
        from ..entity.requests.package import Package
        if self.packages is None:
            self.packages = []
        # Создаем или обновляем первую упаковку
        if not self.packages:
            self.packages.append(Package(weight=weight))
        else:
            self.packages[0].weight = weight
        return self
