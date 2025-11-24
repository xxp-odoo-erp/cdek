from pydantic import BaseModel, Field

from .enums import WebhookType


class WebhookRequest(BaseModel):
    """Модель запроса на добавление подписки на webhook"""

    type: WebhookType = Field(..., description="Тип вебхука")
    url: str = Field(..., description="URL, на который отправляется событие")
