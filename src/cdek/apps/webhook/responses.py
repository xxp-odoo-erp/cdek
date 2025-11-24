from __future__ import annotations

from uuid import UUID

from pydantic import BaseModel, Field

from ..models.entity_response import EntityResponse
from .enums import WebhookType


class WebhookResponse(BaseModel):
    """Модель ответа о списке webhooks."""

    uuid: UUID = Field(..., description="Идентификатор вебхука")
    type: WebhookType = Field(..., description="Тип вебхука")
    url: str = Field(..., description="URL, на который отправляется событие")


class WebookSetEntityResponse(EntityResponse):
    """Ответ на добавление подписки на webhook"""


class WebhookUUIDEntityResponse(EntityResponse):
    """Ответ на получение информации о подписке по UUID"""

    entity: WebhookResponse | None = Field(default=None, description="Webhook")


class WebhookDeleteEntityResponse(EntityResponse):
    """Ответ на удаление подписки на webhook"""
