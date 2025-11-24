from __future__ import annotations

from datetime import date as Date
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
    package_id: UUID | None = Field(
        None,
        description="Уникальный номер упаковки в ИС СДЭК",
    )
    weight: int | None = Field(
        None,
        description="Общий вес упаковки (в граммах)",
    )
    length: int | None = Field(
        None,
        description="Длина упаковки (в сантиметрах)",
    )
    width: int | None = Field(
        None,
        description="Ширина упаковки (в сантиметрах)",
    )
    height: int | None = Field(
        None,
        description="Высота упаковки (в сантиметрах)",
    )


class IntakesEntity(BaseModel):
    order_uuid: UUID = Field(..., alias="uuid")
    intake_number: str | None = Field(
        None, max_length=255, description="Номер заявки в системе СДЭК"
    )
    to_location: IntakeLocation | None = Field(None, description="Место доставки")
    statuses: list[Status] | None = Field(None, description="Статусы заявки")
    packages: list[IntakePackage] | None = Field(
        None, description="Список упаковок заявки"
    )
    contragent_uuid: UUID | None = Field(None, description="Идентификатор контрагента")


class IntakeEntityResponse(EntityResponse):
    entity: IntakesEntity | None = None


class IntakeDateResponse(BaseModel):
    date: list[Date] = Field(..., description="Доступные даты для забора курьером")
    all_days: bool | None = Field(None, description="Все дни")
    errors: list[Error] | None = Field(None, description="Ошибки")
    warnings: list[WarningModel] | None = Field(None, description="Предупреждения")
