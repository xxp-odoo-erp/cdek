from __future__ import annotations

from typing import Any
from unittest.mock import MagicMock, patch

import pytest

from cdek.exceptions import CdekRequestException

INVALID_UUID = "00000000-0000-0000-0000-000000000000"
MOSCOW_CITY_CODE = 44
SAMARA_CITY_CODE = 430
CDEK_NUMBER = "1109677077"


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


def _mock_success_response(payload: dict[str, Any]) -> MagicMock:
    """Создать мок успешного ответа API CDEK."""
    response = MagicMock()
    response.status_code = 200
    response.json.return_value = payload
    response.headers = {}
    return response


def _mock_moscow_to_samara_order_response() -> dict[str, Any]:
    """
    Ответ API для заказа Москва — Самара.

    from_location без address воспроизводит issue #23:
    https://github.com/xxp-odoo-erp/cdek/issues/23
    """
    return {
        "entity": {
            "uuid": "88a05818-c832-447b-a7a5-8561d3fd2b47",
            "type": 1,
            "tariff_code": 139,
            "number": "TEST-123",
            "cdek_number": int(CDEK_NUMBER),
            "statuses": [{"code": "CREATED", "name": "Создан"}],
            "recipient": {
                "name": "Получатель",
                "phones": [{"number": "+79997654321"}],
            },
            "packages": [],
            "from_location": {
                "code": MOSCOW_CITY_CODE,
                "city_uuid": "7e8f36ba-d937-4ce4-8d53-e44177db6469",
                "city": "Москва",
                "latitude": 55.75222,
                "longitude": 37.61556,
                "country_code": "RU",
                "country": "Россия",
                "region": "Москва",
            },
            "to_location": {
                "code": SAMARA_CITY_CODE,
                "city_uuid": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
                "city": "Самара",
                "latitude": 53.195,
                "longitude": 50.1069,
                "country_code": "RU",
                "country": "Россия",
                "region": "Самарская область",
                "address": "ул. Молодогвардейская, д. 210",
            },
        }
    }


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


def test_order_get_by_cdek_number_moscow_to_samara(test_client) -> None:  # type: ignore
    """
    Тест get_by_cdek_number для отправки Москва — Самара с использованием моков.
    """
    order_app = test_client.order

    with patch.object(order_app, "_session") as mock_session:
        mock_session.post.return_value = _mock_auth_response()
        mock_session.request.return_value = _mock_success_response(
            _mock_moscow_to_samara_order_response()
        )

        order_info = order_app.get_by_cdek_number(CDEK_NUMBER)

    assert order_info.entity is not None
    assert order_info.entity.cdek_number == int(CDEK_NUMBER)
    assert order_info.entity.from_location is not None
    assert order_info.entity.from_location.code == MOSCOW_CITY_CODE
    assert order_info.entity.from_location.city == "Москва"
    assert order_info.entity.from_location.address is None
    assert order_info.entity.to_location is not None
    assert order_info.entity.to_location.code == SAMARA_CITY_CODE
    assert order_info.entity.to_location.city == "Самара"
