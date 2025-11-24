from __future__ import annotations

from datetime import date as Date

from pydantic import BaseModel, Field, field_serializer


class WorkTime(BaseModel):
    day: int = Field(..., description="Порядковый номер дня начиная с единицы")
    time: str = Field(..., max_length=255, description="Период работы в эти дни")


class WorkTimeException(BaseModel):
    date_start: Date = Field(..., description="Дата начала исключения в работе офиса")
    date_end: Date = Field(..., description="Дата окончания исключения в работе офиса")
    time_start: str | None = Field(
        None, description="Время начала работы в указанную дату"
    )
    time_end: str | None = Field(
        None, description="Время окончания работы в указанную дату"
    )
    is_working: bool = Field(
        ..., description="Признак рабочего/нерабочего дня в указанную дату"
    )

    @field_serializer("date_start")
    def serialize_date_start(self, date_start: Date) -> str:
        """Представить дату начала исключения в формате ISO"""
        return date_start.strftime("%Y-%m-%d")

    @field_serializer("date_end")
    def serialize_date_end(self, date_end: Date) -> str:
        """Представить дату окончания исключения в формате ISO"""
        return date_end.strftime("%Y-%m-%d")
