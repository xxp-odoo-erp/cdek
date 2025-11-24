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


def test_invoice_get_unknown_uuid(test_client) -> None:  # type: ignore
    """Тест получения накладной с невалидным UUID с использованием моков."""
    invoice_app = test_client.invoice

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
    with patch.object(invoice_app, "_session") as mock_session:
        mock_session.post.return_value = _mock_auth_response()
        mock_session.request.return_value = error_response

        with pytest.raises(CdekRequestException):
            invoice_app.get(INVALID_UUID)


def test_invoice_get_pdf_unknown_uuid(test_client) -> None:  # type: ignore
    """Тест получения PDF накладной с невалидным UUID с использованием моков."""
    invoice_app = test_client.invoice

    # Настраиваем мок для ошибки API - для PDF запросов ошибка возвращается как JSON
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
    with patch.object(invoice_app, "_session") as mock_session:
        mock_session.post.return_value = _mock_auth_response()
        mock_session.request.return_value = error_response

        with pytest.raises(CdekRequestException):
            invoice_app.get_pdf(INVALID_UUID)
