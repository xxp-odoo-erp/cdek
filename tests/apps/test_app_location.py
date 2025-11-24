from __future__ import annotations

from unittest.mock import MagicMock, patch

from cdek.apps.location.filters import CityFilter


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


def test_location_city_returns_moscow(test_client) -> None:  # type: ignore
    """Тест получения города Москва с использованием моков."""
    location_app = test_client.location

    # Настраиваем мок для успешного ответа API согласно структуре CDEK API
    # В API приходит UUID как строка
    success_response = MagicMock()
    success_response.status_code = 200
    success_response.json.return_value = {
        "code": 44,
        "city_uuid": "89b75a9b-d5ae-49ad-8ae6-476bb9c6122e",
        "full_name": "г. Москва",
        "country_code": "RU",
    }
    success_response.headers = {}

    # Мокируем сессию
    with patch.object(location_app, "_session") as mock_session:
        mock_session.post.return_value = _mock_auth_response()
        mock_session.request.return_value = success_response

        city = location_app.city(CityFilter(name="Москва"))

        assert city is not None
        assert city.code == 44
        assert city.full_name == "г. Москва"


def test_location_regions_returns_data(test_client) -> None:  # type: ignore
    """Тест получения списка регионов с использованием моков."""
    location_app = test_client.location

    # Настраиваем мок для успешного ответа API
    success_response = MagicMock()
    success_response.status_code = 200
    success_response.json.return_value = [
        {
            "region": "Московская область",
            "region_code": 77,
            "country": "Россия",
            "country_code": "RU",
        },
        {
            "region": "Ленинградская область",
            "region_code": 78,
            "country": "Россия",
            "country_code": "RU",
        },
    ]
    success_response.headers = {}

    # Мокируем сессию
    with patch.object(location_app, "_session") as mock_session:
        mock_session.post.return_value = _mock_auth_response()
        mock_session.request.return_value = success_response

        regions = location_app.regions()

        assert isinstance(regions, list)
        assert len(regions) > 0
