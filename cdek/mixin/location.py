from dataclasses import dataclass

@dataclass
class Location:
    """LocationTrait - функционал включён в классы"""

    code: int | None = None
    postal_code: str | None = None
    longitude: float | None = None
    latitude: float | None = None
    country_code: str | None = None
    country: str | None = None
    region: str | None = None
    region_code: int | None = None
    sub_region: str | None = None
    city: str | None = None
    kladr_code: str | None = None
    address: str | None = None
    postal_codes: list | None = None
