from datetime import datetime

from pydantic import Field, field_serializer

from ..models.contact import ContragentType
from ..models.location import Coordinates, Zip
from ..models.package import CalcPackage
from ..request import BaseRequest


class CalculatorLocation(BaseRequest, Zip, Coordinates):
    code: int | None = Field(None, description="Код населенного пункта СДЭК")
    country_code: str | None = Field(
        None, max_length=2, description="Код страны в формате ISO_3166-1_alpha-2"
    )
    city: str | None = Field(None, description="Название населенного пункта")
    address: str | None = Field(None, description="Адрес населенного пункта")
    contragent_type: ContragentType | None = Field(None, description="Тип контрагента")


class TariffListRequest(BaseRequest):
    date: datetime | None = Field(
        None,
        description="Дата и время планируемой передачи заказа",
    )
    type: int = Field(
        1,
        description="Тип заказа. 1 — интернет-магазин, 2 — доставка. По умолчанию — 1.",
    )
    additional_order_types: list[int] | None = Field(
        None,
        description="Дополнительные типы заказа",
    )
    currency: int | None = Field(
        None,
        description=("Валюта расчетаПо умолчанию — валюта договора."),
    )
    lang: str = Field(
        "rus",
        max_length=3,
        description="Язык вывода информации о тарифах. "
        "Возможные значения: rus, eng, zho",
    )
    from_location: CalculatorLocation | None = Field(
        None, description="Отправляющий адрес"
    )
    to_location: CalculatorLocation | None = Field(None, description="Получающий адрес")
    packages: list[CalcPackage] | None = Field(None, description="Список упаковок")

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
    code: str | None = Field(None, description="Код дополнительной услуги")
    parameter: str | None = Field(None, description="Параметр дополнительной услуги")


class TariffCodeRequest(TariffListRequest):
    tariff_code: int = Field(..., description="Код тарифа")
    services: list[CalcAdditionalService] | None = Field(
        None, description="Список дополнительных услуг"
    )
