from __future__ import annotations

from datetime import date as Date
from datetime import datetime as DateTime
from uuid import UUID

from pydantic import BaseModel, Field, field_serializer

from ..models.error import Error
from ..models.warning import WarningModel


class PaymentOrder(BaseModel):
    order_uuid: UUID = Field(
        ...,
        description="Идентификатор заказа в ИС СДЭК. "
        "Обязателен, если не указан номер заказа",
    )
    cdek_number: int = Field(
        ...,
        description="Номер заказа СДЭК. Обязателен, "
        "если не указан идентификатор заказа",
    )
    number: str = Field(..., description="Номер заказа в ИС Клиента")


class PaymentInfoResponse(BaseModel):
    orders: list[PaymentOrder] | None = Field(None, description="Список заказов")
    errors: list[Error] | None = Field(None, description="Список ошибок")
    warnings: list[WarningModel] | None = Field(
        None, description="Список предупреждений"
    )


class RegistryOrder(BaseModel):
    cdek_number: str = Field(
        ...,
        description="Номер заказа СДЭК. Обязателен, "
        "если не указан идентификатор заказа",
    )
    transfer_sum: float = Field(
        ..., description="Сумма к начислению (в валюте взаиморасчетов)"
    )
    payment_sum: float = Field(
        ...,
        description="Сумма наложенного платежа, которую взяли с получателя"
        " (в валюте взаиморасчетов)",
    )
    total_sum_without_agent: float = Field(
        ...,
        description="Итоговая стоимость заказа без учета агентского вознаграждения"
        " (в валюте взаиморасчетов)",
    )
    agent_commission_sum: float = Field(
        ...,
        description="Агентское вознаграждение по переводу наложенного платежа "
        " (в валюте взаиморасчетов)",
    )


class Registry(BaseModel):
    registry_number: int = Field(..., description="Номер реестра наложенного платежа")
    payment_date: Date | None = Field(
        None, description="Фактическая дата оплаты реестра наложенного платежа"
    )
    sum: float = Field(..., description="Сумма по реестру (в валюте взаиморасчетов)")
    payment_order_number: str | None = Field(
        None,
        description=(
            "Номер платежного поручения, в рамках которого был осуществлен платеж. "
            "Если атрибут отсутствует или пустой, свяжитесь со своим менеджером"
        ),
    )
    orders: list[RegistryOrder] = Field(..., description="Список заказов реестра")
    date_created: DateTime | None = Field(
        None, description="Дата создания реестра наложенного платежа"
    )

    @field_serializer("date_created")
    def serialize_date_created(self, date_created: DateTime) -> str:
        """Вернуть дату создания реестра в формате ISO 8601"""
        return date_created.strftime("%Y-%m-%dT%H:%M:%S")

    @field_serializer("payment_date")
    def serialize_payment_date(self, payment_date: Date) -> str:
        """Представить дату оплаты реестра в формате YYYY-MM-DD"""
        return payment_date.strftime("%Y-%m-%d")


class PaymentResponse(BaseModel):
    registries: list[Registry] | None = Field(None, description="Список реестров")
    errors: list[Error] | None = Field(None, description="Список ошибок")
    warnings: list[WarningModel] | None = Field(
        None, description="Список предупреждений"
    )
