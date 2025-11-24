from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest

from cdek.exceptions import CdekRequestException

INVALID_UUID = "00000000-0000-0000-0000-000000000000"


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


def test_order_get_by_uuid_unknown_order(test_client) -> None:  # type: ignore
    """Тест получения заказа по UUID с невалидным UUID с использованием моков."""
    order_app = test_client.order

    # Настраиваем мок для ошибки API согласно структуре CDEK API
    error_response = MagicMock()
    error_response.status_code = 404
    error_response.json.return_value = {
        "errors": [
            {
                "code": "ORDER_NOT_FOUND",
                "message": "Заказ не найден",
                "additional_code": "ORD-001",
            }
        ]
    }
    error_response.headers = {}

    # Мокируем сессию
    with patch.object(order_app, "_session") as mock_session:
        mock_session.post.return_value = _mock_auth_response()
        mock_session.request.return_value = error_response

        with pytest.raises(CdekRequestException):
            order_app.get_by_uuid(INVALID_UUID)


def test_order_get_by_cdek_number_unknown_order(test_client) -> None:  # type: ignore
    """
    Тест получения заказа по номеру СДЭК
    с невалидным номером с использованием моков.
    """
    order_app = test_client.order

    # Настраиваем мок для ошибки API
    error_response = MagicMock()
    error_response.status_code = 404
    error_response.json.return_value = {
        "errors": [
            {
                "code": "ORDER_NOT_FOUND",
                "message": "Заказ не найден",
                "additional_code": "ORD-001",
            }
        ]
    }
    error_response.headers = {}

    # Мокируем сессию
    with patch.object(order_app, "_session") as mock_session:
        mock_session.post.return_value = _mock_auth_response()
        mock_session.request.return_value = error_response

        with pytest.raises(CdekRequestException):
            order_app.get_by_cdek_number("0000000000")
