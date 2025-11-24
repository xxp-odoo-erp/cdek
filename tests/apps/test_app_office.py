from __future__ import annotations

from unittest.mock import MagicMock, patch
from uuid import uuid4

from cdek.apps.location.filters import CityFilter
from cdek.apps.office.filters import OfficeFilter


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


def test_office_get_returns_points_for_moscow(test_client) -> None:  # type: ignore
    """Тест получения ПВЗ для Москвы с использованием моков."""
    location_app = test_client.location
    office_app = test_client.office

    # Настраиваем мок для получения города
    # В API приходит UUID как строка
    city_response = MagicMock()
    city_response.status_code = 200
    city_response.json.return_value = {
        "code": 44,
        "city_uuid": "6b88cb14-0669-4ae3-9ded-1d7843d40ac8",
        "full_name": "г. Москва",
        "country_code": "RU",
    }
    city_response.headers = {}

    # Настраиваем мок для получения ПВЗ согласно структуре CDEK API
    offices_response = MagicMock()
    offices_response.status_code = 200
    offices_response.json.return_value = [
        {
            "code": "MSK1",
            "uuid": str(uuid4()),
            "address_comment": "ул. Тестовая, д. 1",
            "nearest_station": "Станция метро",
            "work_time": "пн-пт 9-18",
            "phones": [{"number": "+79991234567"}],
            "type": "PVZ",
            "owner_code": "CDEK",
            "take_only": False,
            "is_handout": True,
            "is_reception": True,
            "is_dressing_room": True,
            "have_cashless": True,
            "have_cash": True,
            "have_fast_payment_system": True,
            "allowed_cod": True,
            "work_time_list": [],
            "work_time_exception_list": [],
            "location": {
                "code": 44,
                "city_code": 44,
                "city_uuid": "6b88cb14-0669-4ae3-9ded-1d7843d40ac8",
                "city": "Москва",
                "country_code": "RU",
            },
        }
    ]
    offices_response.headers = {}

    # Мокируем сессии для обоих приложений
    with (
        patch.object(location_app, "_session") as mock_location_session,
        patch.object(office_app, "_session") as mock_office_session,
    ):
        mock_location_session.post.return_value = _mock_auth_response()
        mock_location_session.request.return_value = city_response

        mock_office_session.post.return_value = _mock_auth_response()
        mock_office_session.request.return_value = offices_response

        city = location_app.city(CityFilter(name="Москва"))
        assert city is not None

        result = office_app.get(OfficeFilter(city_code=city.code, size=5))

        assert "result" in result
        assert isinstance(result["result"], list)
        assert len(result["result"]) > 0
