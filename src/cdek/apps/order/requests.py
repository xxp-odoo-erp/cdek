from __future__ import annotations

from pydantic import Field

from ..models.order import Order, UpdateOrder


class OrderRequest(Order):
    """Модель для запроса на создание заказа."""

    print: str | None = Field(None, description="Тип печатной формы")
    widget_token: str | None = Field(None, description="Токен CMS")


class OrderUpdateRequest(UpdateOrder):
    """Изменение заказа"""

    uuid: str | None = Field(None, description="Идентификатор заказа в ИС СДЭК")
    cdek_number: int | None = Field(None, description="Номер заказа в ИС СДЭК")
