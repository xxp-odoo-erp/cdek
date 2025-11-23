from __future__ import annotations

from typing import Optional

from uuid import UUID

from pydantic import BaseModel, Field

from ..models.location import City, Coordinates, Country, Region


class CityResponse(BaseModel):
    code: int = Field(..., description="Код населенного пункта СДЭК")
    city_uuid: UUID = Field(
        ..., max_length=255, description="Идентификатор населенного пункта СДЭК"
    )
    full_name: str = Field(
        ...,
        max_length=255,
        description="Наименование населенного пункта СДЭК",
    )
    country_code: str = Field(
        ..., max_length=255, description="Код страны в формате ISO_3166-1_alpha-2"
    )


class RegionResponse(Country, Region):
    pass


class ZipResponse(BaseModel):
    code: int = Field(
        ..., description="Код города, которому принадлежат почтовые индексы"
    )
    postal_code: list[str] = Field(..., description="Почтовые индексы города")


class CoordinatesResponse(City):
    pass


class CitiesResponse(City, Country, Region, Coordinates):
    region: Optional[str] = Field(
        default=None, max_length=255, description="Название региона"
    )
    time_zone: Optional[str] = Field(None, description="Часовой пояс населенного пункта")
    payment_limit: Optional[float] = Field(
        ..., description="Ограничение на сумму наложенного платежа в населенном пункте"
    )
