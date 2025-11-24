from __future__ import annotations

from typing import Literal
from uuid import UUID

from pydantic import BaseModel, Field


class OfficeFilter(BaseModel):
    """Фильтр для ПВЗ"""

    code: str | None = Field(None, max_length=255, description="Код ПВЗ")
    type: Literal["PVZ", "POSTAMAT", "ALL"] = Field("ALL", description="Тип офиса")
    postal_code: str | None = Field(
        None,
        max_length=255,
        description="Почтовый индекс города, для которого необходим список офисов",
    )
    city_code: int | None = Field(
        None,
        description='Код населенного пункта СДЭК (метод "Список населенных пунктов")',
    )
    country_code: str | None = Field(
        None,
        max_length=2,
        description="Код страны в формате ISO_3166-1_alpha-2",
    )
    region_code: int | None = Field(None, description="Код региона СДЭК")
    have_cashless: bool | None = Field(None, description="Наличие терминала оплаты")
    have_cash: bool | None = Field(None, description="Есть прием наличных")
    is_dressing_room: bool | None = Field(None, description="Наличие примерочной")
    weight_max: int | None = Field(
        None, gt=0, description="Максимальный вес в кг, который может принять офис"
    )
    weight_min: int | None = Field(
        None, gt=0, description="Минимальный вес в кг, который может принять офис"
    )
    lang: str = Field("rus", description="Локализация офиса")
    take_only: bool | None = Field(
        None, description="Является ли офис только пунктом выдачи"
    )
    is_handout: bool | None = Field(None, description="Является пунктом выдачи")
    is_reception: bool | None = Field(None, description="Есть ли в офисе приём заказов")
    is_marketplace: bool | None = Field(
        None, description='Офис для доставки "До маркетплейса"'
    )
    is_ltl: bool | None = Field(
        None, description="Работает ли офис с LTL (сборный груз)"
    )
    fulfillment: bool | None = Field(None, description="Офис с зоной фулфилмента")
    fias_guid: UUID | None = Field(None, description="Код города ФИАС")
    size: int | None = Field(
        None, ge=0, description="Ограничение выборки результата (размер страницы)"
    )
    page: int | None = Field(
        None, ge=0, description="Номер страницы выборки результата"
    )
