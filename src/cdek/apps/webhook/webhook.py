from __future__ import annotations

from ..app import App
from .requests import WebhookRequest
from .responses import (
    WebhookDeleteEntityResponse,
    WebhookResponse,
    WebhookUUIDEntityResponse,
    WebookSetEntityResponse,
)


class WebhookApp(App):
    """Класс для работы с webhook"""

    def all(self) -> list[WebhookResponse]:
        """Информация о слушателях webhook"""
        response = self._get("webhooks")
        return [WebhookResponse.model_validate(item) for item in response]

    def get(self, uuid: str) -> WebhookUUIDEntityResponse:
        """
        Информация о слушателе webhook

        Args:
            uuid: идентификатор слушателя webhook

        Returns:
            WebhookUUIDEntityResponse: объект с информацией о слушателе webhook
        """
        response = self._get(f"webhooks/{uuid}")
        return WebhookUUIDEntityResponse.model_validate(response)

    def delete(self, uuid: str) -> WebhookDeleteEntityResponse:
        """
        Удаление слушателя webhook

        Args:
            uuid: идентификатор слушателя webhook

        Returns:
            WebhookDeleteEntityResponse: объект с информацией о удаленном
                слушателе webhook
        """
        if not isinstance(uuid, str):
            raise ValueError("uuid must be a str")
        response = self._delete(f"webhooks/{uuid}")
        return WebhookDeleteEntityResponse.model_validate(response)

    def set(self, webhook: WebhookRequest) -> WebookSetEntityResponse:
        """
        Добавление нового слушателя webhook

        Args:
            webhook: объект WebhookRequest с параметрами запроса

        Returns:
            WebookSetEntityResponse: объект с информацией о добавленном
            слушателе webhook

        Raises:
            ValueError: если webhook не является объектом WebhookRequest
        """
        if not isinstance(webhook, WebhookRequest):
            raise ValueError("webhook must be a WebhookRequest")
        response = self._post("webhooks", json=webhook)
        return WebookSetEntityResponse.model_validate(response)
