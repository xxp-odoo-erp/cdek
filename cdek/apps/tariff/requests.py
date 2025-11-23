from __future__ import annotations

from typing import Optional

from datetime import datetime

from pydantic import Field, field_serializer

from ..models.contact import ContragentType
from ..models.location import Coordinates, Zip
from ..models.package import CalcPackage
from ..request import BaseRequest


class CalculatorLocation(BaseRequest, Zip, Coordinates):
    code: Optional[int] = Field(default=None, description="Код населенного пункта СДЭК")
    country_code: Optional[str] = Field(
        default=None, max_length=2, description="Код страны в формате ISO_3166-1_alpha-2"
    )
    city: Optional[str] = Field(default=None, description="Название населенного пункта")
    address: Optional[str] = Field(default=None, description="Адрес населенного пункта")
    contragent_type: Optional[ContragentType] = Field(default=None, description="Тип контрагента")


class TariffListRequest(BaseRequest):
    date: Optional[datetime] = Field(
        None,
        description="Дата и время планируемой передачи заказа",
    )
    type: int = Field(
        1,
        description="Тип заказа. 1 — интернет-магазин, 2 — доставка. По умолчанию — 1.",
    )
    additional_order_types: Optional[list[int]] = Field(
        None,
        description="Дополнительные типы заказа",
    )
    currency: Optional[int] = Field(
        None,
        description=("Валюта расчетаПо умолчанию — валюта договора."),
    )
    lang: str = Field(
        "rus",
        max_length=3,
        description="Язык вывода информации о тарифах. "
        "Возможные значения: rus, eng, zho",
    )
    from_location: Optional[CalculatorLocation] = Field(
        None, description="Отправляющий адрес"
    )
    to_location: Optional[CalculatorLocation] = Field(None, description="Получающий адрес")
    packages: Optional[list[CalcPackage]] = Field(None, description="Список упаковок")

    def set_city_codes(self, from_location: int, to_location: int):
        """Задать коды населённых пунктов отправителя и получателя"""
        self.from_location = CalculatorLocation.init(code=from_location)
        self.to_location = CalculatorLocation.init(code=to_location)
        return self

    def set_package_weight(self, weight: int):
        """Определить вес единственной упаковки в граммах"""
        self.packages = [CalcPackage.init(weight=weight)]
        return self

    @field_serializer("date")
    def serialize_date(self, date: datetime) -> str:
        """Сериализовать дату в формат, поддерживаемый API"""
        return date.strftime("%Y-%m-%dT%H:%M:%S")


class CalcAdditionalService(BaseRequest):
    code: Optional[str] = Field(None, description="Код дополнительной услуги")
    parameter: Optional[str] = Field(None, description="Параметр дополнительной услуги")


class TariffCodeRequest(TariffListRequest):
    tariff_code: int = Field(..., description="Код тарифа")
    services: Optional[list[CalcAdditionalService]] = Field(
        None, description="Список дополнительных услуг"
    )
