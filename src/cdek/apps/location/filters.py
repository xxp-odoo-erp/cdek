from __future__ import annotations

from typing import Literal
from uuid import UUID

from pydantic import BaseModel, Field


class CityFilter(BaseModel):
    """Фильтр для городов"""

    name: str = Field(..., description="Наименование населенного пункта СДЭК")
    country_code: str | None = Field(
        None, description="Код страны в формате ISO_3166-1_alpha-2"
    )


class CityListFilter(BaseModel):
    """Фильтр для списка городов"""

    country_codes: str | None = Field(
        None, description="Массив кодов стран в формате ISO_3166-1_alpha-2"
    )
    region_code: int | None = Field(None, description="Код региона (справочник СДЭК)")
    kladr_region_code: str | None = Field(None, description="Код КЛАДР региона")
    kladr_code: str | None = Field(None, description="Код КЛАДР населенного пункта")
    fias_guid: UUID | None = Field(
        None, description="Уникальный идентификатор ФИАС населенного пункта"
    )
    postal_code: str | None = Field(None, description="Почтовый индекс")
    code: int | None = Field(None, description="Код населенного пункта СДЭК")
    city: str | None = Field(
        None,
        description="Название населенного пункта. Должно соответствовать полностью",
    )
    payment_limit: float | None = Field(
        None, description="Ограничение на сумму наложенного платежа"
    )
    size: int | None = Field(1000, description="Ограничение выборки результата")
    page: int | None = Field(
        0, description="Номер страницы выборки результата. Нумерация страниц с 0"
    )
    lang: str | None = Field(None, description="Язык локализации ответа")


class RegionFilter(BaseModel):
    """Фильтр для регионов"""

    country_codes: str | None = Field(
        None, description="Список кодов стран в формате ISO_3166-1_alpha-2"
    )
    size: int = Field(1000, description="Ограничение выборки результата")
    page: int = Field(0, description="Номер страницы выборки результата")
    lang: Literal["rus", "zho"] = Field("rus", description="Локализация")


class ZipFilter(BaseModel):
    """Фильтр для почтовых индексов"""

    city_code: int = Field(
        ..., description="Код города, которому принадлежат почтовые индексы"
    )


class CoordinatesFilter(BaseModel):
    """Фильтр для координат"""

    latitude: float = Field(..., description="Широта")
    longitude: float = Field(..., description="Долгота")
