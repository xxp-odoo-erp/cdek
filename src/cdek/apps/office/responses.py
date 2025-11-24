from __future__ import annotations

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
    region: str | None = Field(default=None)  # type: ignore
    city: str | None = Field(default=None)  # type: ignore


class OfficeResponse(BaseModel):
    """Модель ответа офиса"""

    code: str = Field(..., description="Код ПВЗ")
    uuid: str = Field(..., description="Идентификатор офиса в ИС СДЭК")
    address_comment: str | None = Field(None, description="Описание местоположения")
    nearest_station: str | None = Field(
        None, description="Ближайшая станция/остановка транспорта"
    )
    nearest_metro_station: str | None = Field(
        None, description="Ближайшая станция метро"
    )
    work_time: str = Field(
        ..., description="Режим работы, строка вида «пн-пт 9-18, сб 9-16»"
    )
    phones: list[Phone] | None = Field(default=None, description="Телефоны офиса")
    email: str | None = Field(None, description="Адрес электронной почты")
    note: str | None = Field(None, description="Примечание по ПВЗ")
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
    is_marketplace: bool | None = Field(
        None, description='Офис для доставки заказов "До маркетплейса"'
    )
    is_ltl: bool | None = Field(
        None, description="Работает ли офис с LTL (сборный груз)"
    )
    have_cashless: bool = Field(..., description="Есть безналичный расчет")
    have_cash: bool = Field(..., description="Есть приём наличных")
    have_fast_payment_system: bool = Field(
        ..., description="Есть безналичный расчёт по СБП"
    )
    allowed_cod: bool = Field(..., description="Разрешен наложенный платеж в ПВЗ")
    site: str | None = Field(None, description="Ссылка на данный офис на сайте СДЭК")
    office_image_list: list[Image] | None = Field(
        None, description="Все фото офиса (кроме фото как доехать)"
    )
    work_time_list: list[WorkTime] = Field(..., description="График работы на неделю")
    work_time_exception_list: list[WorkTimeException] = Field(
        ..., description="Исключения из графика работы"
    )
    weight_min: float | None = Field(
        None, description="Минимальный вес (в кг.), принимаемый в ПВЗ (> WeightMin)"
    )
    weight_max: float | None = Field(
        None, description="Максимальный вес (в кг.), принимаемый в ПВЗ (<= WeightMax)"
    )
    dimensions: list[Dimensions] | None = Field(None, description="Размеры ПВЗ")
    errors: list[Error] | None = Field(None, description="Список ошибок")
    warnings: list[WarningModel] | None = Field(
        None, description="Список предупреждений"
    )
    location: OfficeLocation = Field(..., description="Информация об офисе")
    distance: int | None = Field(
        None, description="Расстояние до точки, поиск ближайшего ПВЗ"
    )
    fulfillment: bool | None = Field(
        None, description='Работает ли офис с "Фулфилмент. Приход"'
    )
