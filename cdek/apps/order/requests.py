from __future__ import annotations

from typing import Optional

from pydantic import Field

from ..models.order import Order, UpdateOrder
from ..request import BaseRequest


class OrderRequest(BaseRequest, Order):
    """Модель для запроса на создание заказа."""

    print: Optional[str] = Field(None, description="Тип печатной формы")
    widget_token: Optional[str] = Field(
        None, description="Токен CMS"
    )


class OrderUpdateRequest(BaseRequest, UpdateOrder):
    """Изменение заказа"""

    uuid: Optional[str] = Field(None, description="Идентификатор заказа в ИС СДЭК")
    cdek_number: Optional[int] = Field(None, description="Номер заказа в ИС СДЭК")
