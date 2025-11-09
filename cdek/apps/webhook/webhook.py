from ..app import App
from .requests import WebhookRequest
from .responses import (
    WebhookDeleteEntityResponse,
    WebhookResponse,
    WebhookUUIDEntityResponse,
    WebookSetEntityResponse,
)


class WebhookApp(App):
    webhook = WebhookRequest

    def all(self):
        """Информация о слушателях webhook"""
        response = self._api_request("GET", self.constants.WEBHOOKS_URL)
        return [WebhookResponse.model_validate(item) for item in response]

    def get(self, uuid: str):
        """Информация о слушателе webhook"""
        response = self._api_request("GET", f"{self.constants.WEBHOOKS_URL}/{uuid}")
        return WebhookUUIDEntityResponse.model_validate(response)

    def delete(self, uuid: str):
        """Удаление слушателя webhook"""
        response = self._api_request("DELETE", f"{self.constants.WEBHOOKS_URL}/{uuid}")
        return WebhookDeleteEntityResponse.model_validate(response)

    def set(self, webhook: "WebhookRequest"):
        """Добавление нового слушателя webhook"""
        response = self._api_request(
            "POST", self.constants.WEBHOOKS_URL, webhook.model_dump()
            )
        return WebookSetEntityResponse.model_validate(response)
