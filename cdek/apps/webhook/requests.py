from pydantic import Field

from ..request import BaseRequest
from .enums import WebhookType


class WebhookRequest(BaseRequest):
    """Модель запроса на добавление подписки на webhook"""

    type: WebhookType = Field(..., description="Тип вебхука")
    url: str = Field(..., description="URL, на который отправляется событие")
