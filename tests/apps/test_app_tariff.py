from __future__ import annotations

from unittest.mock import MagicMock, patch

from cdek.apps.tariff.responses import AvailableTariff


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


def test_tariff_all_returns_available_tariffs(test_client) -> None:  # type: ignore
    """Тест получения списка доступных тарифов с использованием моков."""
    tariff_app = test_client.tariff

    # Настраиваем мок для успешного ответа API согласно структуре CDEK API
    # Метод all() возвращает TariffAvailableResponse с AvailableTariff
    success_response = MagicMock()
    success_response.status_code = 200
    success_response.json.return_value = {
        "tariff_codes": [
            {
                "tariff_name": "Посылка склад-склад",
                "weight_min": 1.0,
                "weight_max": 30.0,
            },
            {
                "tariff_name": "Посылка склад-дверь",
                "weight_min": 1.0,
                "weight_max": 30.0,
            },
        ]
    }
    success_response.headers = {}

    # Мокируем сессию
    with patch.object(tariff_app, "_session") as mock_session:
        mock_session.post.return_value = _mock_auth_response()
        mock_session.request.return_value = success_response

        response = tariff_app.all()

        codes = response.get_codes()
        assert isinstance(codes, list)
        assert len(codes) > 0
        assert isinstance(codes[0], AvailableTariff)
