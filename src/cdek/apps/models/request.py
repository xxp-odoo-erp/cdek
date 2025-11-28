from __future__ import annotations

from datetime import datetime
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, Field, field_serializer

from .error import Error
from .warning import WarningModel


class Request(BaseModel):
    """Модель ответа о запросе."""

    request_uuid: UUID | None = Field(
        None, description="Идентификатор запроса в ИС СДЭК"
    )
    type: Literal[
        "CREATE",
        "UPDATE",
        "DELETE",
        "AUTH",
        "GET",
        "CREATE_CLIENT_RETURN",
        "CREATE_REFUSAL",
    ] = Field(..., description="Тип запроса")
    date_time: datetime = Field(
        ..., description="Дата и время установки текущего состояния запроса"
    )
    state: Literal["ACCEPTED", "WAITING", "SUCCESSFUL", "INVALID"] = Field(
        ..., max_length=255, description="Текущее состояние запроса"
    )
    errors: list[Error] | None = Field(
        None, description="Ошибки, возникшие в ходе выполнения запроса"
    )
    warnings: list[WarningModel] | None = Field(
        None, description="Предупреждения, возникшие в ходе выполнения запроса"
    )

    def get_state(self) -> str | None:
        """Получить состояние запроса."""
        return self.state

    @field_serializer("date_time")
    def serialize_date_time(self, date_time: datetime) -> str:
        """Представить дату последнего изменения запроса в формате ISO"""
        return date_time.strftime("%Y-%m-%dT%H:%M:%S")
