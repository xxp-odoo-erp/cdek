from __future__ import annotations

from datetime import date as Date
from datetime import datetime
from typing import Optional

from pydantic import Field, field_serializer

from ..models.entity_response import EntityResponse
from ..models.order import (
    AccompanyingWaybill,
    Call,
    DeliveryDetail,
    DeliveryProblem,
    Order,
    OrderStatus,
)


class OrderResponse(Order):
    """Модель ответа о заказе."""

    uuid: str = Field(..., description="Идентификатор заказа в ИС СДЭК")
    type: int = Field(..., description="Тип заказа")
    is_return: bool = Field(..., description="Признак возврата заказа")
    is_reverse: bool = Field(..., description="Признак реверсного заказа")
    cdek_number: Optional[int] = Field(..., description="Номер заказа в ИС СДЭК")
    accompanying_waybill: Optional[AccompanyingWaybill] = Field(
        None, description="Информация для сопроводительной накладной"
    )
    keep_free_until: Optional[datetime] = Field(
        None, description="Дата окончания бесплатного хранения"
    )
    statuses: list[OrderStatus] = Field(..., description="Статусы заказа")
    is_client_return: bool = Field(..., description="Признак клиентского возврата")
    delivery_mode: Optional[str] = Field(None, description="Режим доставки")
    planned_delivery_date: Optional[Date] = Field(
        None, description="Планируемая дата доставки"
    )
    delivery_detail: Optional[DeliveryDetail] = Field(
        None, description="Детальная информация о доставке"
    )
    transacted_payment: Optional[bool] = Field(
        None, description="Признак проведенного платежа"
    )
    delivery_problem: Optional[DeliveryProblem] = Field(
        None, description="Проблема с доставкой"
    )
    developer_key: Optional[str] = Field(None, description="Ключ разработчика")
    calls: Optional[Call] = Field(None, description="Информация о прозвонах")

    @field_serializer("planned_delivery_date")
    def serialize_planned_delivery_date(self, planned_delivery_date: Date) -> str:
        """Вернуть плановую дату доставки в формате YYYY-MM-DD"""
        return planned_delivery_date.strftime("%Y-%m-%d")

    @field_serializer("keep_free_until")
    def serialize_keep_free_until(self, keep_free_until: datetime) -> str:
        """Представить дату окончания бесплатного хранения в формате ISO 8601"""
        return keep_free_until.strftime("%Y-%m-%dT%H:%M:%S")


class OrderEntityResponse(EntityResponse):
    """Модель ответа о заказе."""

    entity: Optional[OrderResponse] = Field(
        default=None, description="Информация о заказе в рамках протокола"
    )
