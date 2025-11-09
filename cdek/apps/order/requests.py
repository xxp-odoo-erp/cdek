from __future__ import annotations

from pydantic import Field

from ..models.order import Order, UpdateOrder
from ..request import BaseRequest


class OrderRequest(BaseRequest, Order):
    """Модель для запроса на создание заказа."""

    print: str | None = Field(None, description="Тип печатной формы")
    widget_token: str | None = Field(
        None, description="Токен CMS"
    )


class OrderUpdateRequest(BaseRequest, UpdateOrder):
    """Изменение заказа"""

    uuid: str | None = Field(None, description="Идентификатор заказа в ИС СДЭК")
    cdek_number: int | None = Field(None, description="Номер заказа в ИС СДЭК")
