from __future__ import annotations

import json
from datetime import datetime
from typing import Any
from uuid import UUID

import pytest
from pydantic import ValidationError

from cdek.apps.webhook import (
    AccompanyingWaybillEvent,
    CourierInfoEvent,
    DelivAgreementEvent,
    DelivProblemEvent,
    DownloadPhotoEvent,
    OfficeAvailabilityEvent,
    OrderModifiedEvent,
    OrderStatusEvent,
    PrealertClosedEvent,
    PrintFormEvent,
    ReceiptEvent,
    WebhookType,
    parse_webhook,
)

ORDER_STATUS_PAYLOAD: dict[str, Any] = {
    "type": "ORDER_STATUS",
    "date_time": "2023-11-28T07:44:45+0000",
    "uuid": "72753031-1820-4f99-9240-aab139f05ca5",
    "attributes": {
        "is_return": False,
        "is_reverse": False,
        "is_client_return": False,
        "cdek_number": "1100285492",
        "number": "17011574744791",
        "related_entities": [],
        "code": "RECEIVED_AT_SHIPMENT_WAREHOUSE",
        "status_code": "3",
        "status_date_time": "2023-11-28T07:44:45+0000",
        "city_name": "Новосибирск",
        "city_code": "270",
        "deleted": False,
    },
}

ORDER_MODIFIED_PAYLOAD: dict[str, Any] = {
    "type": "ORDER_MODIFIED",
    "date_time": "2024-08-19T10:02:15+0000",
    "uuid": "72753034-23a3-46a5-974d-8b1239d515e1",
    "attributes": {
        "modification_type": "PLANED_DELIVERY_DATE_CHANGED",
        "new_value": {"type": "DATE", "value": "2024-08-21"},
    },
}

PRINT_FORM_PAYLOAD: dict[str, Any] = {
    "type": "PRINT_FORM",
    "date_time": "2023-11-28T09:03:31+0000",
    "uuid": "72753031-e1f1-4fc8-97ee-d58a010b6a67",
    "attributes": {
        "type": "BARCODE",
        "url": (
            "http://api.cdek.ru/v2/print/barcodes/"
            "72753031-e1f1-4fc8-97ee-d58a010b6a67.pdf"
        ),
    },
}

DOWNLOAD_PHOTO_PAYLOAD: dict[str, Any] = {
    "type": "DOWNLOAD_PHOTO",
    "date_time": "2026-01-01T10:11:12+0700",
    "uuid": "72753031-6417-44d2-8c0d-649a1d4b4721",
    "attributes": {
        "cdek_number": "10123456789",
        "link": "https://api.cdek.ru/v2/photoDocument/72753031-e1f1-4fc8-97ee-d58a010b6a68",
        "create_date": "2026-01-01T10:11:12+0000",
    },
}

PREALERT_CLOSED_PAYLOAD: dict[str, Any] = {
    "type": "PREALERT_CLOSED",
    "date_time": "2023-01-23T10:20:02+0000",
    "uuid": "72753031-a1d3-4266-bc9f-8052f0fc3b2c",
    "attributes": {
        "prealert_number": "PA/7/583",
        "closed_date": "2023-01-17T07:59:18+0000",
        "fact_shipment_point": "NSK1",
    },
}

ACCOMPANYING_WAYBILL_PAYLOAD: dict[str, Any] = {
    "type": "ACCOMPANYING_WAYBILL",
    "date_time": "2024-08-01T05:40:09+0000",
    "uuid": "72753034-7bb8-4221-bf65-5b4ab9ddb15a",
    "attributes": {
        "cdek_number": "10000000123",
        "client_name": "Имя Клиента",
        "flight_number": "S511111",
        "air_waybill_numbers": ["A1111111", "B5263589"],
        "planned_departure_date_time": "2024-08-05T13:00:00+0000",
    },
}

OFFICE_AVAILABILITY_PAYLOAD: dict[str, Any] = {
    "type": "OFFICE_AVAILABILITY",
    "date_time": "2024-08-19T03:01:10+0000",
    "uuid": "fc3ef89a-0727-4a26-8d07-81a0bfd11d22",
    "attributes": {"type": "AVAILABLE_OFFICE", "code": "MSK123"},
}

DELIV_PROBLEM_PAYLOAD: dict[str, Any] = {
    "type": "DELIV_PROBLEM",
    "date_time": "2024-12-18T07:49:33+0000",
    "uuid": "72753031-a5c5-4e30-8234-bd9daf53ad59",
    "attributes": {
        "cdek_number": "10000077777",
        "number": "IM-123456789",
        "code": "45",
        "create_date": "2024-12-18T11:35:57Z",
    },
}

DELIV_AGREEMENT_PAYLOAD: dict[str, Any] = {
    "type": "DELIV_AGREEMENT",
    "date_time": "2024-12-06T11:32:31+0000",
    "uuid": "72753031-680b-47dd-83e7-027e35e831b3",
    "attributes": {
        "delivery_uuid": "72753031-68d6-4d18-b52a-45e9da153bdc",
        "date_time": "2024-12-06T11:32:31.608716Z",
        "cdek_number": "10000063729",
        "date": "2024-12-13",
        "time_from": "11:00:00",
        "time_to": "18:00:00",
        "comment": "Доставка до двери",
        "source": "EK5_INTEGRATION",
        "type": "DOOR",
    },
}

COURIER_INFO_PAYLOAD: dict[str, Any] = {
    "type": "COURIER_INFO",
    "date_time": "2026-01-27T11:51:13+0000",
    "uuid": "26d20be9-01b9-4283-bb13-d5a91e90c4e4",
    "attributes": {
        "task_type": "DELIVERY",
        "cdek_number": "10000000123",
        "courier": {
            "name": "",
            "car_model": "",
            "registration_mark": "",
            "phone": "+79999999999, доб. 123",
        },
    },
}

RECEIPT_PAYLOAD: dict[str, Any] = {
    "type": "RECEIPT",
    "date_time": "2024-01-01T12:00:00+0000",
    "uuid": "72753031-0000-4000-8000-000000000001",
    "attributes": {"cdek_number": "10000000001", "unknown_field": "ok"},
}


@pytest.mark.parametrize(
    ("payload", "expected_type"),
    [
        (ORDER_STATUS_PAYLOAD, OrderStatusEvent),
        (ORDER_MODIFIED_PAYLOAD, OrderModifiedEvent),
        (PRINT_FORM_PAYLOAD, PrintFormEvent),
        (DOWNLOAD_PHOTO_PAYLOAD, DownloadPhotoEvent),
        (PREALERT_CLOSED_PAYLOAD, PrealertClosedEvent),
        (ACCOMPANYING_WAYBILL_PAYLOAD, AccompanyingWaybillEvent),
        (OFFICE_AVAILABILITY_PAYLOAD, OfficeAvailabilityEvent),
        (DELIV_PROBLEM_PAYLOAD, DelivProblemEvent),
        (DELIV_AGREEMENT_PAYLOAD, DelivAgreementEvent),
        (COURIER_INFO_PAYLOAD, CourierInfoEvent),
        (RECEIPT_PAYLOAD, ReceiptEvent),
    ],
)
def test_parse_webhook_official_examples(
    payload: dict[str, Any], expected_type: type[Any]
) -> None:
    """Все официальные примеры разбираются в ожидаемый тип события."""
    event = parse_webhook(payload)
    assert isinstance(event, expected_type)
    assert isinstance(event.date_time, datetime)
    assert isinstance(event.uuid, UUID)


def test_parse_webhook_accepts_json_string_and_bytes() -> None:
    """parse_webhook принимает str и bytes."""
    as_str = json.dumps(ORDER_STATUS_PAYLOAD)
    as_bytes = as_str.encode("utf-8")

    event_from_str = parse_webhook(as_str)
    event_from_bytes = parse_webhook(as_bytes)

    assert isinstance(event_from_str, OrderStatusEvent)
    assert isinstance(event_from_bytes, OrderStatusEvent)
    assert event_from_str.attributes.cdek_number == "1100285492"


def test_order_status_fields() -> None:
    """Поля ORDER_STATUS соответствуют примеру из документации."""
    event = parse_webhook(ORDER_STATUS_PAYLOAD)
    assert isinstance(event, OrderStatusEvent)
    assert event.type == WebhookType.ORDER_STATUS
    assert event.attributes.code == "RECEIVED_AT_SHIPMENT_WAREHOUSE"
    assert event.attributes.status_code == "3"
    assert event.attributes.city_name == "Новосибирск"
    assert event.attributes.deleted is False


def test_order_modified_new_value() -> None:
    """ORDER_MODIFIED содержит new_value с типом и значением."""
    event = parse_webhook(ORDER_MODIFIED_PAYLOAD)
    assert isinstance(event, OrderModifiedEvent)
    assert event.attributes.modification_type.value == "PLANED_DELIVERY_DATE_CHANGED"
    assert event.attributes.new_value.type.value == "DATE"
    assert event.attributes.new_value.value == "2024-08-21"


def test_extra_fields_are_ignored() -> None:
    """Лишние поля в payload не ломают разбор."""
    attributes: dict[str, Any] = dict(ORDER_STATUS_PAYLOAD["attributes"])
    attributes["future_field"] = "value"
    payload: dict[str, Any] = {**ORDER_STATUS_PAYLOAD, "attributes": attributes}
    event = parse_webhook(payload)
    assert isinstance(event, OrderStatusEvent)


def test_unknown_type_raises() -> None:
    """Неизвестный type вызывает ValidationError."""
    payload = {
        "type": "UNKNOWN_EVENT",
        "date_time": "2024-01-01T00:00:00+0000",
        "uuid": "72753031-0000-4000-8000-000000000099",
        "attributes": {},
    }
    with pytest.raises(ValidationError):
        parse_webhook(payload)


def test_webhook_type_contains_courier_info() -> None:
    """WebhookType включает COURIER_INFO."""
    assert WebhookType.COURIER_INFO.value == "COURIER_INFO"


def test_receipt_allows_extra_attributes() -> None:
    """RECEIPT сохраняет дополнительные атрибуты."""
    event = parse_webhook(RECEIPT_PAYLOAD)
    assert isinstance(event, ReceiptEvent)
    assert event.attributes.model_extra is not None
    assert event.attributes.model_extra.get("unknown_field") == "ok"
    assert event.attributes.model_extra.get("cdek_number") == "10000000001"
