from __future__ import annotations

from datetime import date as Date
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field

from ..models.entity_response import EntityResponse
from ..models.error import Error
from ..models.intakes import IntakeLocation, Intakes
from ..models.status import Status
from ..models.warning import WarningModel


class IntakesResponse(Intakes):
    pass


class IntakePackage(BaseModel):
    package_id: Optional[UUID] = Field(
        None,
        description="Уникальный номер упаковки в ИС СДЭК",
    )
    weight: Optional[int] = Field(
        None,
        description="Общий вес упаковки (в граммах)",
    )
    length: Optional[int] = Field(
        None,
        description="Длина упаковки (в сантиметрах)",
    )
    width: Optional[int] = Field(
        None,
        description="Ширина упаковки (в сантиметрах)",
    )
    height: Optional[int] = Field(
        None,
        description="Высота упаковки (в сантиметрах)",
    )


class IntakesEntity(BaseModel):
    order_uuid: UUID = Field(..., alias="uuid")
    intake_number: Optional[str] = Field(
        None, max_length=255, description="Номер заявки в системе СДЭК"
    )
    to_location: Optional[IntakeLocation] = Field(None, description="Место доставки")
    statuses: Optional[list[Status]] = Field(None, description="Статусы заявки")
    packages: Optional[list[IntakePackage]] = Field(
        None, description="Список упаковок заявки"
    )
    contragent_uuid: Optional[UUID] = Field(None, description="Идентификатор контрагента")


class IntakeEntityResponse(EntityResponse):
    entity: Optional[IntakesEntity] = None


class IntakeDateResponse(BaseModel):
    date: list[Date] = Field(..., description="Доступные даты для забора курьером")
    all_days: Optional[bool] = Field(None, description="Все дни")
    errors: Optional[list[Error]] = Field(None, description="Ошибки")
    warnings: Optional[list[WarningModel]] = Field(None, description="Предупреждения")
