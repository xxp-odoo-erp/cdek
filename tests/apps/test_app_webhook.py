from __future__ import annotations

from unittest.mock import MagicMock, patch
from uuid import uuid4

from cdek.client import CdekClient


def _mock_auth_response() -> MagicMock:
    """Создать мок ответа авторизации согласно API CDEK."""
    response = MagicMock()
    response.status_code = 200
    response.json.return_value = {
        "access_token": "test_access_token_12345",
        "token_type": "Bearer",
        "expires_in": 3600,
        "scope": "test_scope",
    }
    return response


def test_webhook_all_returns_list(test_client: CdekClient) -> None:
    """Тест получения списка вебхуков с использованием моков."""
    webhook_app = test_client.webhook

    # Настраиваем мок для успешного ответа API согласно структуре CDEK API
    success_response = MagicMock()
    success_response.status_code = 200
    success_response.json.return_value = [
        {
            "uuid": str(uuid4()),
            "type": "ORDER_STATUS",
            "url": "https://example.com/webhook",
        },
        {
            "uuid": str(uuid4()),
            "type": "PREALERT_CLOSED",
            "url": "https://example.com/webhook2",
        },
    ]
    success_response.headers = {}

    # Мокируем сессию
    with patch.object(webhook_app, "_session") as mock_session:
        mock_session.post.return_value = _mock_auth_response()
        mock_session.request.return_value = success_response

        webhooks = webhook_app.all()

        assert isinstance(webhooks, list)
        assert len(webhooks) > 0
