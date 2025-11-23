from __future__ import annotations

from typing import Optional

from typing import Literal
from uuid import UUID

from pydantic import Field

from ..request import BaseRequest


class CityFilter(BaseRequest):
    """Фильтр для городов"""

    name: str = Field(..., description="Наименование населенного пункта СДЭК")
    country_code: Optional[str] = Field(
        None, description="Код страны в формате ISO_3166-1_alpha-2"
    )


class CityListFilter(BaseRequest):
    """Фильтр для списка городов"""

    country_codes: Optional[str] = Field(
        None, description="Массив кодов стран в формате ISO_3166-1_alpha-2"
    )
    region_code: Optional[int] = Field(None, description="Код региона (справочник СДЭК)")
    kladr_region_code: Optional[str] = Field(None, description="Код КЛАДР региона")
    kladr_code: Optional[str] = Field(None, description="Код КЛАДР населенного пункта")
    fias_guid: Optional[UUID] = Field(
        None, description="Уникальный идентификатор ФИАС населенного пункта"
    )
    postal_code: Optional[str] = Field(None, description="Почтовый индекс")
    code: Optional[int] = Field(None, description="Код населенного пункта СДЭК")
    city: Optional[str] = Field(
        None,
        description="Название населенного пункта. Должно соответствовать полностью",
    )
    payment_limit: Optional[float] = Field(
        None, description="Ограничение на сумму наложенного платежа"
    )
    size: Optional[int] = Field(1000, description="Ограничение выборки результата")
    page: Optional[int] = Field(
        0, description="Номер страницы выборки результата. Нумерация страниц с 0"
    )
    lang: Optional[str] = Field(None, description="Язык локализации ответа")


class RegionFilter(BaseRequest):
    """Фильтр для регионов"""

    country_codes: Optional[str] = Field(
        None, description="Список кодов стран в формате ISO_3166-1_alpha-2"
    )
    size: int = Field(1000, description="Ограничение выборки результата")
    page: int = Field(0, description="Номер страницы выборки результата")
    lang: Literal["rus", "zho"] = Field("rus", description="Локализация")


class ZipFilter(BaseRequest):
    """Фильтр для почтовых индексов"""

    city_code: int = Field(
        ..., description="Код города, которому принадлежат почтовые индексы"
    )


class CoordinatesFilter(BaseRequest):
    """Фильтр для координат"""

    latitude: float = Field(..., description="Широта")
    longitude: float = Field(..., description="Долгота")
