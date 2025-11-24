from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field

from ..models.error import Error
from ..models.warning import WarningModel


class DeliveryDateRange(BaseModel):
    min: str | None = Field(None, description="Минимальная дата доставки")
    max: str | None = Field(None, description="Максимальная дата доставки")


class TariffListItem(BaseModel):
    """Модель элемента списка тарифов."""

    tariff_code: int = Field(
        ..., description="Код тарифа. Обязателен для расчета по коду тарифа"
    )
    tariff_name: str = Field(
        ..., max_length=255, description="Название тарифа на языке вывода"
    )
    tariff_description: str | None = Field(
        None, max_length=255, description="Описание тарифа на языке вывода"
    )
    delivery_mode: int = Field(..., description="Режим тарифа (справочник СДЭК)")
    delivery_sum: float = Field(..., description="Стоимость доставки")
    period_min: int = Field(
        ..., description="Минимальное время доставки (в рабочих днях)"
    )
    period_max: int = Field(
        ..., description="Максимальное время доставки (в рабочих днях)"
    )
    calendar_min: int | None = Field(
        None, description="Минимальное время доставки (в календарных днях)"
    )
    calendar_max: int | None = Field(
        None, description="Максимальное время доставки (в календарных днях)"
    )
    delivery_date_range: DeliveryDateRange | None = Field(
        None, description="Прогнозируемый диапазон дат доставки"
    )


class TariffListResponse(BaseModel):
    """Модель ответа со списком тарифов."""

    tariff_codes: list[TariffListItem] | None = Field(default_factory=list)
    errors: list[Error] | None = Field(None, description="Список ошибок")
    warnings: list[WarningModel] | None = Field(
        None, description="Список предупреждений"
    )

    def get_codes(self) -> list[TariffListItem]:
        """Вернуть список тарифов, гарантируя, что результат не None"""
        return self.tariff_codes or []


class Services(BaseModel):
    """Модель ответа для дополнительных услуг."""

    code: str = Field(..., description="Тип дополнительной услуги")
    sum: float = Field(..., description="Стоимость услуги")
    total_sum: float = Field(..., description="Стоимость услуги с НДС и скидкой")
    discount_percent: float = Field(..., description="Процент скидки")
    discount_sum: float = Field(..., description="Сумма скидки")
    vat_rate: float = Field(..., description="Ставка НДС")
    vat_sum: float = Field(..., description="Сумма НДС")


class TariffResponse(BaseModel):
    delivery_sum: float = Field(..., description="Стоимость доставки")
    period_min: int = Field(
        ..., description="Минимальное время доставки (в рабочих днях)"
    )
    period_max: int = Field(
        ..., description="Максимальное время доставки (в рабочих днях)"
    )
    calendar_min: int | None = Field(
        None, description="Минимальное время доставки (в календарных днях)"
    )
    calendar_max: int | None = Field(
        None, description="Максимальное время доставки (в календарных днях)"
    )
    weight_calc: int = Field(..., description="Расчетный вес (в граммах)")
    services: list[Services] | None = Field(
        None,
        description="Дополнительные услуги "
        "(возвращается, если в запросе были переданы доп. услуги)",
    )
    total_sum: float = Field(
        ..., description="Стоимость доставки с учетом дополнительных услуг"
    )
    currency: str = Field(
        ..., description="Валюта, в которой рассчитана стоимость доставки (код СДЭК)"
    )
    errors: list[Error] | None = Field(None, description="Список ошибок")
    warnings: list[WarningModel] | None = Field(
        None, description="Список предупреждений"
    )
    delivery_date_range: DeliveryDateRange | None = Field(
        None, description="Прогнозируемый диапазон дат доставки"
    )

    def get_calendar_min(self) -> int | None:
        """Получить минимальный период доставки."""
        return self.calendar_min

    def get_calendar_max(self) -> int | None:
        """Получить максимальный период доставки."""
        return self.calendar_max


class DeliveryMode(BaseModel):
    """Модель для режима доставки."""

    delivery_mode: str | None = None
    delivery_mode_name: str | None = None
    tariff_code: int | None = None


class AvailableTariff(BaseModel):
    tariff_name: str | None = Field(None, description="Имя сервиса")
    weight_min: float | None = Field(None, description="Минимальный вес отправления")
    weight_max: float | None = Field(None, description="Максимальный вес отправления")
    weight_calc_max: float | None = Field(
        None, description="Максимальный расчётный вес"
    )
    length_min: int | None = Field(None, description="Минимальная длина упаковки")
    length_max: int | None = Field(None, description="Максимальная длина упаковки")
    width_min: int | None = Field(None, description="Минимальная ширина упаковки")
    width_max: int | None = Field(None, description="Максимальная ширина упаковки")
    height_min: int | None = Field(None, description="Минимальная высота упаковки")
    height_max: int | None = Field(None, description="Максимальная высота упаковки")
    order_types: list[str] | None = Field(
        None,
        description="Список доступных типов заказов для тарифа "
        "(пустой список означает отсутствие ограничений)",
    )
    payer_contragent_type: list[str] | None = Field(
        None,
        description=(
            "Список типов контрагентов-плательщиков: "
            "LEGAL_ENTITY — юридическое лицо, INDIVIDUAL — физическое лицо. "
            "Пустой список означает отсутствие ограничений."
        ),
    )
    sender_contragent_type: list[str] | None = Field(
        None,
        description=(
            "Список типов контрагентов-отправителей: "
            "LEGAL_ENTITY — юридическое лицо, INDIVIDUAL — физическое лицо. "
            "Пустой список означает отсутствие ограничений."
        ),
    )
    recipient_contragent_type: list[str] | None = Field(
        None,
        description=(
            "Список типов контрагентов-получателей: LEGAL_ENTITY — юридическое лицо, "
            "INDIVIDUAL — физическое лицо. "
            "Пустой список означает отсутствие ограничений."
        ),
    )
    delivery_modes: list[DeliveryMode] | None = Field(
        None, description="Режимы доставки"
    )
    additional_order_types_param: dict[str, Any] | None = Field(
        None, description="Доп. типы заказа, применимые к тарифу"
    )


class TariffAvailableResponse(BaseModel):
    """Модель ответа о доступных тарифах."""

    tariff_codes: list[AvailableTariff] | None = Field(
        None, description="Список доступных тарифов"
    )

    def get_codes(self) -> list[AvailableTariff]:
        """Вернуть список доступных тарифов без значений None"""
        return self.tariff_codes or []
