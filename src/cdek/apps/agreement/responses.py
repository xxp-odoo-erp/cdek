from __future__ import annotations

from datetime import date as Date
from uuid import UUID

from pydantic import BaseModel, Field, field_serializer

from ..models.status import Status
from .requests import RegisterDeliveryRequest


class AvailableDeliveryInterval(BaseModel):
    start_time: str = Field(..., description="Время начала интервала доставки")
    end_time: str = Field(..., description="Время окончания интервала доставки")


class AvailableDeliveryIntervalsInfo(BaseModel):
    date: Date = Field(
        ..., description="Дата доступного интервала для доставки (формат yyyy-MM-dd)"
    )
    time_intervals: list[AvailableDeliveryInterval] = Field(
        ..., description="Временные интервалы для доставки"
    )

    @field_serializer("date")
    def serialize_date(self, date: Date) -> str:
        """Представить дату интервала доставки в формате YYYY-MM-DD"""
        return date.strftime("%Y-%m-%d")


class AvailableDeliveryIntervalsResponse(BaseModel):
    date_intervals: list[AvailableDeliveryIntervalsInfo] = Field(
        ..., description="Доступные интервалы доставки"
    )


class ScheduleInfoEntity(RegisterDeliveryRequest):
    uuid: UUID = Field(..., description="Идентификатор договоренности о доставке")
    statuses: list[Status] = Field(..., description="Статусы договоренности о доставке")
    source: str | None = Field(
        None,
        description="Источник согласования",
    )


class AgreementInfoResponse(BaseModel):
    entity: ScheduleInfoEntity | None = Field(
        default=None, description="Договорённость о доставке"
    )
