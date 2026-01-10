from __future__ import annotations

from uuid import UUID

from pydantic import BaseModel, Field


class City(BaseModel):
    code: int = Field(..., description="Код населенного пункта СДЭК")
    city_uuid: UUID = Field(
        ..., description="Идентификатор населенного пункта в ИС СДЭК"
    )
    city: str = Field(..., description="Название населенного пункта")
    fias_guid: UUID | None = Field(
        None, description="Уникальный идентификатор ФИАС населенного пункта"
    )


class Region(BaseModel):
    region: str = Field(..., max_length=255, description="Название региона")
    region_code: int | None = Field(None, description="Код региона СДЭК")
    kladr_region_code: str | None = Field(
        None, description="Код КЛАДР региона населенного пункта"
    )
    sub_region: str | None = Field(
        None, description="Название района региона населенного пункта"
    )


class Zip(BaseModel):
    postal_code: str | None = Field(None, description="Почтовые индексы города")


class Country(BaseModel):
    country_code: str | None = Field(
        None, max_length=2, description="Код страны в формате ISO_3166-1_alpha-2"
    )
    country: str | None = Field(
        None, max_length=255, description="Название страны региона"
    )


class Coordinates(BaseModel):
    longitude: float | None = Field(None, description="Долгота населенного пункта")
    latitude: float | None = Field(None, description="Широта населенного пункта")


class Address(BaseModel):
    address: str | None = Field(None, description="Адрес населенного пункта")
    address_full: str | None = Field(
        None, description="Полный адрес с указанием страны, региона, города, и т.д."
    )


class FullLocation(City, Country, Region, Coordinates, Address, Zip):
    pass


class OrderLocation(City, Country, Region, Coordinates, Zip):
    code: int | None = Field(default=None)  # type: ignore
    city_uuid: UUID | None = Field(default=None)  # type: ignore
    region: str | None = Field(default=None)  # type: ignore
    city: str | None = Field(default=None)  # type: ignore
    time_zone: str | None = Field(None, description="Часовой пояс населенного пункта")
    address: str = Field(..., description="Строка адреса")
