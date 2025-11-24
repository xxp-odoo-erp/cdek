from __future__ import annotations

from datetime import date
from unittest.mock import MagicMock, patch

import pytest

from cdek.apps.check.filters import CheckFilter
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


def test_check_request_with_fake_order(test_client) -> None:  # type: ignore
    """Тест получения чека для несуществующего заказа с использованием моков."""
    check_app = test_client.check
    filter_params = CheckFilter(
        order_uuid="00000000-0000-0000-0000-000000000000",
        cdek_number="0000000000",
        date=date.today(),
    )

    # Настраиваем мок для ошибки API согласно структуре CDEK API
    error_response = MagicMock()
    error_response.status_code = 200
    error_response.json.return_value = {
        "check_info": [],
        "errors": [
            {
                "code": "CHECK_NOT_FOUND",
                "message": "Чек не найден для указанного заказа",
                "additional_code": "CHK-001",
            }
        ],
    }
    error_response.headers = {}

    # Мокируем сессию
    with patch.object(check_app, "_session") as mock_session:
        mock_session.post.return_value = _mock_auth_response()
        mock_session.request.return_value = error_response

        with pytest.raises(CdekRequestException):
            check_app.get(filter_params)
