from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..requests.location import Location
    from ..requests.package import Package
    from ..requests.services import Services


@dataclass
class TariffMixin:
    """Mixin for working with tariff calculations."""

    type: int | None = None
    tariff_code: int | None = None
    from_location: 'Location | None' = None
    to_location: 'Location | None' = None
    services: 'list[Services] | None' = None
    packages: 'list[Package] | None' = None
    date: str | None = None
    currency: int | None = None

    def set_type(self, delivery_type: int):
        """Set delivery type (1 = standard, 2 = express)."""
        if delivery_type not in [1, 2]:
            raise ValueError("Invalid type")
        self.type = delivery_type
        return self

    def set_tariff_code(self, tariff_code: int):
        """Set tariff code."""
        self.tariff_code = tariff_code
        return self

    def get_tariff_code(self):
        """Get tariff code."""
        return self.tariff_code

    def add_service(self, service: 'Services'):
        """Add additional service."""
        if self.services is None:
            self.services = []
        self.services.append(service)
        return self

    def add_package(self, package: 'Package'):
        """Add a package."""
        if self.packages is None:
            self.packages = []
        self.packages.append(package)
        return self

    def set_from_location(self, location: 'Location'):
        """Set origin location."""
        self.from_location = location
        return self

    def set_to_location(self, location: 'Location'):
        """Set destination location."""
        self.to_location = location
        return self

    def set_services(self, service: 'Services'):
        """Set additional services."""
        if self.services is None:
            self.services = []
        self.services.append(service)
        return self

    def set_packages(self, package: 'Package'):
        """Set packages."""
        if self.packages is None:
            self.packages = []
        self.packages.append(package)
        return self

    def set_city_codes(self, from_code: int, to_code: int):
        """Set origin and destination city codes."""
        from ..requests.location import Location  # noqa
        self.from_location = None
        self.to_location = None

        self.from_location = Location(code=from_code)
        self.to_location = Location(code=to_code)
        return self

    def set_package_weight(self, weight: int):
        """Set package weight in grams."""
        from ..requests.package import Package  # noqa
        if self.packages is None:
            self.packages = []
        # Create or update the first package
        if not self.packages:
            self.packages.append(Package(weight=weight))
        else:
            self.packages[0].weight = weight
        return self
