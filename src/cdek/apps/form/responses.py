from __future__ import annotations

from datetime import datetime
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, Field, field_serializer

from ..models.entity_response import EntityResponse
from ..models.print import PrintForm, PrintType
from .requests import PrintBarcodeRequest


class PrintStatus(BaseModel):
    code: str = Field(..., description="Код статуса")
    name: str = Field(..., description="Название статуса")
    date_time: datetime = Field(..., description="Дата и время статуса")

    @field_serializer("date_time")
    def serialize_date_time(self, date_time: datetime) -> str:
        """Вернуть дату статуса печатной формы в формате ISO 8601"""
        return date_time.strftime("%Y-%m-%dT%H:%M:%S")


class PrintBarcodeEntity(PrintBarcodeRequest):
    uuid: UUID = Field(..., description="Идентификатор ШК места к заказу")
    url: str | None = Field(None, description="Ссылка на скачивание файла")
    lang: Literal["RUS", "ENG", "DEU", "ITA", "TUR", "CES", "KOR", "LIT", "LAV"] = (
        Field(default="RUS", description="Язык печати")  # type: ignore
    )
    statuses: list[PrintStatus] = Field(..., description="Статус файла")


class PrintBarcodeResponse(EntityResponse):
    entity: PrintBarcodeEntity | None = Field(
        default=None, description="ШК места к заказу"
    )


class WaybillResponse(PrintForm):
    uuid: UUID = Field(..., description="Идентификатор ШК места к заказу")
    type: PrintType | None = Field(None, description="Форма квитанции")
    url: str | None = Field(None, description="Ссылка на скачивание файла")
    statuses: list[PrintStatus] = Field(..., description="Статус файла")


class WaybillEntityResponse(EntityResponse):
    entity: WaybillResponse | None = Field(
        default=None, description="Квитанция к заказу"
    )
