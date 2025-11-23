from __future__ import annotations

from datetime import datetime
from typing import Literal, Optional
from uuid import UUID

from pydantic import BaseModel, Field, field_serializer

from .error import Error
from .warning import WarningModel


class Request(BaseModel):
    """Модель ответа о запросе."""

    request_uuid: Optional[UUID] = Field(
        None, description="Идентификатор запроса в ИС СДЭК"
    )
    type: Literal[
        "CREATE", "UPDATE", "DELETE", "AUTH", "GET", "CREATE_CLIENT_RETURN"
    ] = Field(..., description="Тип запроса")
    date_time: datetime = Field(
        ..., description="Дата и время установки текущего состояния запроса"
    )
    state: Literal["ACCEPTED", "WAITING", "SUCCESSFUL", "INVALID"] = Field(
        ..., max_length=255, description="Текущее состояние запроса"
    )
    errors: Optional[list[Error]] = Field(
        None, description="Ошибки, возникшие в ходе выполнения запроса"
    )
    warnings: Optional[list[WarningModel]] = Field(
        None, description="Предупреждения, возникшие в ходе выполнения запроса"
    )

    def get_state(self) -> Optional[str]:
        """Получить состояние запроса."""
        return self.state

    @field_serializer("date_time")
    def serialize_date_time(self, date_time: datetime) -> str:
        """Представить дату последнего изменения запроса в формате ISO"""
        return date_time.strftime("%Y-%m-%dT%H:%M:%S")
