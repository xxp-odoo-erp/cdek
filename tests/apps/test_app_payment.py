from __future__ import annotations

from datetime import date
from unittest.mock import MagicMock, patch

import pytest

from cdek.exceptions import CdekRequestException


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


def test_payment_get_for_empty_period(test_client) -> None:  # type: ignore
    """
    Тест получения информации о платеже за
    период без данных с использованием моков.
    """
    payment_app = test_client.payment

    # Настраиваем мок для ответа без ошибок, но с пустыми данными
    success_response = MagicMock()
    success_response.status_code = 200
    success_response.json.return_value = {
        "registries": [],
        "errors": [
            {
                "code": "NO_DATA_FOR_PERIOD",
                "message": "Нет данных за указанный период",
                "additional_code": "PAY-001",
            }
        ],
    }
    success_response.headers = {}

    # Мокируем сессию
    with patch.object(payment_app, "_session") as mock_session:
        mock_session.post.return_value = _mock_auth_response()
        mock_session.request.return_value = success_response

        with pytest.raises(CdekRequestException):
            payment_app.get(date.today())


def test_payment_get_registries_for_empty_period(test_client) -> None:  # type: ignore
    """Тест получения реестров платежей за период без данных с использованием моков."""
    payment_app = test_client.payment

    # Настраиваем мок для ответа без ошибок, но с пустыми данными
    success_response = MagicMock()
    success_response.status_code = 200
    success_response.json.return_value = {
        "registries": [],
        "errors": [
            {
                "code": "NO_DATA_FOR_PERIOD",
                "message": "Нет данных за указанный период",
                "additional_code": "PAY-001",
            }
        ],
    }
    success_response.headers = {}

    # Мокируем сессию
    with patch.object(payment_app, "_session") as mock_session:
        mock_session.post.return_value = _mock_auth_response()
        mock_session.request.return_value = success_response

        with pytest.raises(CdekRequestException):
            payment_app.get_registries(date.today())
