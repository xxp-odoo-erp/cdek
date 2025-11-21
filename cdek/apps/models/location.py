from __future__ import annotations

from typing import Optional

from uuid import UUID

from pydantic import BaseModel, Field


class City(BaseModel):
    code: int = Field(..., description="Код населенного пункта СДЭК")
    city_uuid: UUID = Field(
        ..., description="Идентификатор населенного пункта в ИС СДЭК"
    )
    city: str = Field(..., description="Название населенного пункта")
    fias_guid: Optional[UUID] = Field(
        None, description="Уникальный идентификатор ФИАС населенного пункта"
    )


class Region(BaseModel):
    region: str = Field(..., max_length=255, description="Название региона")
    region_code: Optional[int] = Field(None, description="Код региона СДЭК")
    kladr_region_code: Optional[str] = Field(
        None, description="Код КЛАДР региона населенного пункта"
    )
    sub_region: Optional[str] = Field(
        None, description="Название района региона населенного пункта"
    )


class Zip(BaseModel):
    postal_code: Optional[str] = Field(None, description="Почтовые индексы города")


class Country(BaseModel):
    country_code: Optional[str] = Field(
        None, max_length=2, description="Код страны в формате ISO_3166-1_alpha-2"
    )
    country: Optional[str] = Field(
        None, max_length=255, description="Название страны региона"
    )


class Coordinates(BaseModel):
    longitude: Optional[float] = Field(None, description="Долгота населенного пункта")
    latitude: Optional[float] = Field(None, description="Широта населенного пункта")


class Address(BaseModel):
    address: Optional[str] = Field(None, description="Адрес населенного пункта")
    address_full: Optional[str] = Field(
        None, description="Полный адрес с указанием страны, региона, города, и т.д."
    )


class FullLocation(City, Country, Region, Coordinates, Address, Zip):
    pass


class OrderLocation(City, Country, Region, Coordinates, Zip):
    time_zone: Optional[str] = Field(None, description="Часовой пояс населенного пункта")
    address: str = Field(..., description="Строка адреса")
