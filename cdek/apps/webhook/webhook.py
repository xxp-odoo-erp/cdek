from ..app import App
from .requests import WebhookRequest
from .responses import (
    WebhookDeleteEntityResponse,
    WebhookResponse,
    WebhookUUIDEntityResponse,
    WebookSetEntityResponse,
)


class WebhookApp(App):

    def all(self):
        """Информация о слушателях webhook"""
        response = self._get(self.constants.WEBHOOKS_URL)
        return [WebhookResponse.model_validate(item) for item in response]

    def get(self, uuid: str):
        """Информация о слушателе webhook"""
        response = self._get(f"{self.constants.WEBHOOKS_URL}/{uuid}")
        return WebhookUUIDEntityResponse.model_validate(response)

    def delete(self, uuid: str):
        """Удаление слушателя webhook"""
        response = self._delete(f"{self.constants.WEBHOOKS_URL}/{uuid}")
        return WebhookDeleteEntityResponse.model_validate(response)

    def set(self, webhook: "WebhookRequest"):
        """Добавление нового слушателя webhook"""
        response = self._post(self.constants.WEBHOOKS_URL, json=webhook)
        return WebookSetEntityResponse.model_validate(response)
