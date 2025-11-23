from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, Field

from ..models import (
    Dimensions,
    Error,
    FullLocation,
    Image,
    Phone,
    WarningModel,
    WorkTime,
    WorkTimeException,
)


class OfficeLocation(FullLocation):
    """Модель ответа локации офиса"""

    code: int = Field(alias="city_code")
    region: Optional[str] = Field(default=None)
    city: Optional[str] = Field(default=None)



class OfficeResponse(BaseModel):
    """Модель ответа офиса"""

    code: str = Field(..., description="Код ПВЗ")
    uuid: str = Field(..., description="Идентификатор офиса в ИС СДЭК")
    address_comment: Optional[str] = Field(None, description="Описание местоположения")
    nearest_station: Optional[str] = Field(
        None, description="Ближайшая станция/остановка транспорта"
    )
    nearest_metro_station: Optional[str] = Field(
        None, description="Ближайшая станция метро"
    )
    work_time: str = Field(
        ..., description="Режим работы, строка вида «пн-пт 9-18, сб 9-16»"
    )
    phones: Optional[list[Phone]] = Field(default=None, description="Телефоны офиса")
    email: Optional[str] = Field(None, description="Адрес электронной почты")
    note: Optional[str] = Field(None, description="Примечание по ПВЗ")
    type: str = Field(
        ..., description="Тип ПВЗ. PVZ — склад СДЭК, POSTAMAT — постамат СДЭК"
    )
    owner_code: str = Field(..., description="Принадлежность офиса компании")
    take_only: bool = Field(
        ..., description="Является ли офис пунктом выдачи или осуществляет приём грузов"
    )
    is_handout: bool = Field(..., description="Является пунктом выдачи")
    is_reception: bool = Field(..., description="Является пунктом приёма")
    is_dressing_room: bool = Field(..., description="Есть ли примерочная")
    is_marketplace: Optional[bool] = Field(
        None, description='Офис для доставки заказов "До маркетплейса"'
    )
    is_ltl: Optional[bool] = Field(
        None, description="Работает ли офис с LTL (сборный груз)"
    )
    have_cashless: bool = Field(..., description="Есть безналичный расчет")
    have_cash: bool = Field(..., description="Есть приём наличных")
    have_fast_payment_system: bool = Field(
        ..., description="Есть безналичный расчёт по СБП"
    )
    allowed_cod: bool = Field(..., description="Разрешен наложенный платеж в ПВЗ")
    site: Optional[str] = Field(None, description="Ссылка на данный офис на сайте СДЭК")
    office_image_list: Optional[list[Image]] = Field(
        None, description="Все фото офиса (кроме фото как доехать)"
    )
    work_time_list: list[WorkTime] = Field(..., description="График работы на неделю")
    work_time_exception_list: list[WorkTimeException] = Field(
        ..., description="Исключения из графика работы"
    )
    weight_min: Optional[float] = Field(
        None, description="Минимальный вес (в кг.), принимаемый в ПВЗ (> WeightMin)"
    )
    weight_max: Optional[float] = Field(
        None, description="Максимальный вес (в кг.), принимаемый в ПВЗ (<= WeightMax)"
    )
    dimensions: Optional[list[Dimensions]] = Field(None, description="Размеры ПВЗ")
    errors: Optional[list[Error]] = Field(None, description="Список ошибок")
    warnings: Optional[list[WarningModel]] = Field(
        None, description="Список предупреждений"
    )
    location: OfficeLocation = Field(..., description="Информация об офисе")
    distance: Optional[int] = Field(
        None, description="Расстояние до точки, поиск ближайшего ПВЗ"
    )
    fulfillment: Optional[bool] = Field(
        None, description='Работает ли офис с "Фулфилмент. Приход"'
    )
