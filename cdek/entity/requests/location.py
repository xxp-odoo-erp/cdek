from dataclasses import dataclass
from .source import Source
from ...mixin.location import Location as LocationMixin
from ... import constants

@dataclass
class Location(Source, LocationMixin):
    """Класс для работы с локацией"""

    address_full: str | None = None
    fias_region_guid: str | None = None
    kladr_region_code: str | None = None
    country: str | None = None
    country_codes: list[str] | None = None
    payment_limit: float | None = None
    lang: str | None = None
    size: int | None = None
    page: int | None = None
    @classmethod
    def with_code(cls, code: int):
        """Экспресс-метод установки кода"""
        return cls(code=code)

    @classmethod
    def with_postal_code(cls, postal_code: str):
        """Экспресс-метод установки почтового индекса"""
        return cls(postal_code=postal_code)

    @classmethod
    def with_address(cls, address: str):
        """Экспресс-метод установки адреса"""
        return cls(address=address)

    @classmethod
    def with_city(cls, city: str):
        """Экспресс-метод установки города"""
        return cls(city=city)

    def set_code(self, code: int):
        """Установить код"""
        self.code = code
        return self

    def set_country_code(self, country_code: str):
        """Установить код страны"""
        self.country_code = country_code
        return self

    def set_country(self, country: str):
        """Установить страну"""
        self.country = country
        return self

    def set_address(self, address: str):
        """Установить адрес"""
        self.address = address
        return self

    def set_postal_code(self, postal_code: str):
        """Установить почтовый индекс"""
        self.postal_code = postal_code
        return self

    def set_city(self, city: str):
        """Установить город"""
        self.city = city
        return self

    def set_region(self, region: str):
        """Установить регион"""
        self.region = region
        return self

    def cities(self):
        """Установить настройки для городов"""
        self.pattern = constants.CITIES_FILTER
        return self

    def regions(self):
        """Установить настройки для регионов"""
        self.pattern = constants.REGIONS_FILTER
        return self

