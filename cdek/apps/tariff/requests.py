from datetime import datetime

from pydantic import Field, field_serializer

from ..models.contact import ContragentType
from ..models.location import Coordinates, Zip
from ..models.package import CalcPackage
from ..request import BaseRequest


class CalculatorLocation(BaseRequest, Zip, Coordinates):
    code: int | None = Field(None, description="Код населенного пункта СДЭК")
    country_code: str | None = Field(None, max_length=2, description="Код страны в формате ISO_3166-1_alpha-2")
    city: str | None = Field(None, description="Название населенного пункта")
    address: str | None = Field(None, description="Адрес населенного пункта")
    contragent_type: ContragentType | None = Field(None, description="Тип контрагента")


class TariffListRequest(BaseRequest):
    date: datetime | None = Field(
        None,
        description=(
            "Дата и время планируемой передачи заказа (формат yyyy-MM-dd'T'HH:mm:ssZ). "
            'По умолчанию используется текущее значение. Пример: "2025-03-24T14:15:22+0700".'
        ),
    )
    type: int = Field(
        1,
        description="Тип заказа. 1 — интернет-магазин, 2 — доставка. По умолчанию — 1.",
    )
    additional_order_types: list[int] | None = Field(
        None,
        description=(
            "Дополнительные типы заказа: 2 — сборный груз (LTL); 4 — Форвард (Forward); "
            "6 — Фулфилмент. Приход; 7 — Фулфилмент. Отгрузка; 9 — Форвард. Экспресс; "
            "10 — доставка шин по тарифу «Экономичный экспресс»; "
            "11 — «Один офис» (офис отправителя и получателя совпадают); "
            "14 — CDEK.Shopping; 15 — «ТО для последней мили». "
            "Совместимость указана в документации СДЭК."
        ),
    )
    currency: int | None = Field(
        None,
        description=(
            "Валюта расчета (числовой код из «Приложение 14. Код валюты для методов расчета стоимости»). "
            "По умолчанию — валюта договора."
        ),
    )
    lang: str = Field(
        "rus",
        max_length=3,
        description="Язык вывода информации о тарифах. Возможные значения: rus, eng, zho. По умолчанию — rus.",
    )
    from_location: CalculatorLocation | None = Field(None, description="Отправляющий адрес")
    to_location: CalculatorLocation | None = Field(None, description="Получающий адрес")
    packages: list[CalcPackage] | None = Field(None, description="Список упаковок")

    def set_city_codes(self, from_location: int, to_location: int):
        self.from_location = CalculatorLocation(code=from_location)
        self.to_location = CalculatorLocation(code=to_location)
        return self

    def set_package_weight(self, weight: int):
        self.packages = [CalcPackage(weight=weight)]
        return self

    @field_serializer("date")
    def serialize_date(self, date: datetime) -> str:
        return date.strftime("%Y-%m-%dT%H:%M:%S")


class CalcAdditionalService(BaseRequest):
    code: str | None = Field(None, description="Код дополнительной услуги")
    parameter: str | None = Field(None, description="Параметр дополнительной услуги")


class TariffCodeRequest(TariffListRequest):
    tariff_code: int = Field(..., description="Код тарифа")
    services: list[CalcAdditionalService] | None = Field(None, description="Список дополнительных услуг")
