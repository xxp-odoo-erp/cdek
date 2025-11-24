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


def test_intake_get_unknown_uuid(test_client) -> None:  # type: ignore
    """
    Тест получения заявки на вызов курьера
    с невалидным UUID с использованием моков.
    """
    intake_app = test_client.intake

    # Настраиваем мок для ошибки API согласно структуре CDEK API
    error_response = MagicMock()
    error_response.status_code = 404
    error_response.json.return_value = {
        "errors": [
            {
                "code": "INTAKE_NOT_FOUND",
                "message": "Заявка на вызов курьера не найдена",
                "additional_code": "INT-001",
            }
        ]
    }
    error_response.headers = {}

    # Мокируем сессию
    with patch.object(intake_app, "_session") as mock_session:
        mock_session.post.return_value = _mock_auth_response()
        mock_session.request.return_value = error_response

        with pytest.raises(CdekRequestException):
            intake_app.get(INVALID_UUID)


def test_intake_delete_unknown_uuid(test_client) -> None:  # type: ignore
    """
    Тест удаления заявки на вызов курьера
     с невалидным UUID с использованием моков.
    """
    intake_app = test_client.intake

    # Настраиваем мок для ошибки API согласно структуре CDEK API
    # При DELETE может возвращаться ошибка через requests массив
    error_response = MagicMock()
    error_response.status_code = 400
    error_response.json.return_value = {
        "requests": [
            {
                "request_uuid": None,
                "type": "DELETE",
                "date_time": "2024-01-01T00:00:00",
                "state": "INVALID",
                "errors": [
                    {
                        "code": "INTAKE_NOT_FOUND",
                        "message": "Заявка на вызов курьера не найдена",
                        "additional_code": "INT-001",
                    }
                ],
            }
        ]
    }
    error_response.headers = {}

    # Мокируем сессию
    with patch.object(intake_app, "_session") as mock_session:
        mock_session.post.return_value = _mock_auth_response()
        mock_session.request.return_value = error_response

        with pytest.raises(CdekRequestException):
            intake_app.delete(INVALID_UUID)
