"""Модели входящих webhook-событий CDEK API."""

from __future__ import annotations

import json
import re
from datetime import date as Date
from datetime import datetime
from typing import Annotated, Any, Literal
from uuid import UUID

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    TypeAdapter,
    field_validator,
)

from .enums import (
    CourierTaskType,
    DelivAgreementSource,
    DelivAgreementType,
    ModificationType,
    ModificationValueType,
    OfficeAvailabilityType,
    PrintFormType,
    WebhookRelatedEntityType,
    WebhookType,
)

# CDEK часто шлёт offset как +0000 / +0700 без двоеточия.
_OFFSET_WITHOUT_COLON = re.compile(r"([+-]\d{2})(\d{2})$")


def normalize_cdek_datetime(value: Any) -> Any:
    """Нормализовать дату/время из payload CDEK к виду, понятному pydantic."""
    if value is None or isinstance(value, (datetime, Date)):
        return value
    if not isinstance(value, str):
        return value

    text = value.strip()
    if text.endswith("Z"):
        text = text[:-1] + "+00:00"
    else:
        text = _OFFSET_WITHOUT_COLON.sub(r"\1:\2", text)
    return text


class WebhookModel(BaseModel):
    """Базовая модель webhook с мягкой валидацией."""

    model_config = ConfigDict(extra="ignore")


class WebhookRelatedEntity(WebhookModel):
    """Связанная сущность во входящем ORDER_STATUS."""

    type: WebhookRelatedEntityType = Field(..., description="Тип связанной сущности")
    cdek_number: str = Field(..., description="Номер заказа СДЭК")
    uuid: UUID = Field(..., description="Идентификатор сущности в ИС СДЭК")


class OrderStatusAttributes(WebhookModel):
    """Атрибуты события ORDER_STATUS."""

    is_return: bool = Field(..., description="Признак возвратного заказа")
    is_reverse: bool = Field(..., description="Признак реверсного заказа")
    is_client_return: bool = Field(..., description="Признак клиентского возврата")
    cdek_number: str = Field(..., description="Номер заказа СДЭК")
    number: str | None = Field(None, description="Номер заказа в ИС клиента")
    related_entities: list[WebhookRelatedEntity] | None = Field(
        None, description="Связанные сущности"
    )
    code: str = Field(..., description="Код статуса заказа")
    status_code: str = Field(..., description="Код статуса")
    status_reason_code: str | None = Field(
        None, description="Дополнительный код статуса"
    )
    status_date_time: datetime = Field(
        ..., description="Дата и время установки статуса"
    )
    city_name: str | None = Field(None, description="Название города")
    city_code: str | None = Field(None, description="Код города СДЭК")
    city_uuid: str | None = Field(None, description="UUID города")
    deleted: bool | None = Field(None, description="Признак удаления статуса")

    @field_validator("status_date_time", mode="before")
    @classmethod
    def _normalize_status_date_time(cls, value: Any) -> Any:
        return normalize_cdek_datetime(value)


class OrderModifiedValue(WebhookModel):
    """Новое значение в событии ORDER_MODIFIED."""

    type: ModificationValueType = Field(..., description="Тип значения")
    value: str = Field(..., description="Значение")


class OrderModifiedAttributes(WebhookModel):
    """Атрибуты события ORDER_MODIFIED."""

    modification_type: ModificationType = Field(..., description="Тип изменения")
    new_value: OrderModifiedValue = Field(..., description="Новое значение")


class PrintFormAttributes(WebhookModel):
    """Атрибуты события PRINT_FORM."""

    type: PrintFormType = Field(..., description="Тип печатной формы")
    url: str = Field(..., description="URL для скачивания печатной формы")


class DownloadPhotoAttributes(WebhookModel):
    """Атрибуты события DOWNLOAD_PHOTO."""

    cdek_number: str = Field(..., description="Номер заказа СДЭК")
    link: str = Field(..., description="Ссылка на фото документа")
    create_date: datetime | None = Field(None, description="Дата создания фото")

    @field_validator("create_date", mode="before")
    @classmethod
    def _normalize_create_date(cls, value: Any) -> Any:
        return normalize_cdek_datetime(value)


class PrealertClosedAttributes(WebhookModel):
    """Атрибуты события PREALERT_CLOSED."""

    prealert_number: str = Field(..., description="Номер преалерта")
    closed_date: datetime = Field(..., description="Дата закрытия преалерта")
    fact_shipment_point: str = Field(..., description="Фактический код ПВЗ отправления")

    @field_validator("closed_date", mode="before")
    @classmethod
    def _normalize_closed_date(cls, value: Any) -> Any:
        return normalize_cdek_datetime(value)


class AccompanyingWaybillAttributes(WebhookModel):
    """Атрибуты события ACCOMPANYING_WAYBILL."""

    cdek_number: str = Field(..., description="Номер заказа СДЭК")
    client_name: str = Field(..., description="Наименование клиента")
    flight_number: str | None = Field(None, description="Номер рейса")
    air_waybill_numbers: list[str] | None = Field(
        None, description="Накладные перевозчика"
    )
    vehicle_numbers: list[str] | None = Field(None, description="Номера автомобилей")
    vehicle_driver: str | None = Field(None, description="Водитель")
    planned_departure_date_time: datetime = Field(
        ..., description="Планируемая дата отправления"
    )

    @field_validator("planned_departure_date_time", mode="before")
    @classmethod
    def _normalize_planned_departure(cls, value: Any) -> Any:
        return normalize_cdek_datetime(value)


class OfficeAvailabilityAttributes(WebhookModel):
    """Атрибуты события OFFICE_AVAILABILITY."""

    type: OfficeAvailabilityType = Field(..., description="Тип изменения доступности")
    code: str = Field(..., description="Код офиса СДЭК")


class DelivProblemAttributes(WebhookModel):
    """Атрибуты события DELIV_PROBLEM."""

    cdek_number: str = Field(..., description="Номер заказа СДЭК")
    number: str | None = Field(None, description="Номер заказа в ИС клиента")
    code: str = Field(..., description="Код проблемы доставки")
    create_date: datetime = Field(..., description="Дата создания проблемы")

    @field_validator("create_date", mode="before")
    @classmethod
    def _normalize_create_date(cls, value: Any) -> Any:
        return normalize_cdek_datetime(value)


class DelivAgreementAttributes(WebhookModel):
    """Атрибуты события DELIV_AGREEMENT."""

    delivery_uuid: UUID = Field(..., description="Идентификатор договорённости")
    date_time: datetime = Field(..., description="Дата и время события")
    cdek_number: str = Field(..., description="Номер заказа СДЭК")
    date: Date | None = Field(None, description="Согласованная дата доставки")
    time_from: str | None = Field(None, description="Начало временного окна")
    time_to: str | None = Field(None, description="Конец временного окна")
    comment: str | None = Field(None, description="Комментарий")
    source: DelivAgreementSource | str = Field(..., description="Источник")
    type: DelivAgreementType = Field(..., description="Тип доставки")
    delivery_point: str | None = Field(None, description="Код ПВЗ")

    @field_validator("date_time", mode="before")
    @classmethod
    def _normalize_date_time(cls, value: Any) -> Any:
        return normalize_cdek_datetime(value)


class CourierInfo(WebhookModel):
    """Данные курьера в событии COURIER_INFO."""

    name: str | None = Field(None, description="ФИО курьера")
    car_model: str | None = Field(None, description="Модель автомобиля")
    registration_mark: str | None = Field(None, description="Гос. номер")
    phone: str | None = Field(None, description="Телефон курьера")


class CourierInfoAttributes(WebhookModel):
    """Атрибуты события COURIER_INFO."""

    task_type: CourierTaskType | str = Field(..., description="Тип задачи")
    cdek_number: str = Field(..., description="Номер заказа СДЭК")
    courier: CourierInfo = Field(..., description="Информация о курьере")


class ReceiptAttributes(WebhookModel):
    """Атрибуты события RECEIPT (схема в публичных примерах не зафиксирована)."""

    model_config = ConfigDict(extra="allow")


class WebhookEventBase(WebhookModel):
    """Базовый конверт входящего webhook-события."""

    date_time: datetime = Field(..., description="Дата и время события")
    uuid: UUID = Field(..., description="Идентификатор сущности события")

    @field_validator("date_time", mode="before")
    @classmethod
    def _normalize_date_time(cls, value: Any) -> Any:
        return normalize_cdek_datetime(value)


class OrderStatusEvent(WebhookEventBase):
    """Событие изменения статуса заказа."""

    type: Literal[WebhookType.ORDER_STATUS] = WebhookType.ORDER_STATUS
    attributes: OrderStatusAttributes


class OrderModifiedEvent(WebhookEventBase):
    """Событие изменения данных заказа."""

    type: Literal[WebhookType.ORDER_MODIFIED] = WebhookType.ORDER_MODIFIED
    attributes: OrderModifiedAttributes


class PrintFormEvent(WebhookEventBase):
    """Событие готовности печатной формы."""

    type: Literal[WebhookType.PRINT_FORM] = WebhookType.PRINT_FORM
    attributes: PrintFormAttributes


class DownloadPhotoEvent(WebhookEventBase):
    """Событие готовности фото документов."""

    type: Literal[WebhookType.DOWNLOAD_PHOTO] = WebhookType.DOWNLOAD_PHOTO
    attributes: DownloadPhotoAttributes


class PrealertClosedEvent(WebhookEventBase):
    """Событие закрытия преалерта."""

    type: Literal[WebhookType.PREALERT_CLOSED] = WebhookType.PREALERT_CLOSED
    attributes: PrealertClosedAttributes


class AccompanyingWaybillEvent(WebhookEventBase):
    """Событие сопроводительной накладной."""

    type: Literal[WebhookType.ACCOMPANYING_WAYBILL] = WebhookType.ACCOMPANYING_WAYBILL
    attributes: AccompanyingWaybillAttributes


class OfficeAvailabilityEvent(WebhookEventBase):
    """Событие изменения доступности офиса."""

    type: Literal[WebhookType.OFFICE_AVAILABILITY] = WebhookType.OFFICE_AVAILABILITY
    attributes: OfficeAvailabilityAttributes


class DelivProblemEvent(WebhookEventBase):
    """Событие проблемы доставки."""

    type: Literal[WebhookType.DELIV_PROBLEM] = WebhookType.DELIV_PROBLEM
    attributes: DelivProblemAttributes


class DelivAgreementEvent(WebhookEventBase):
    """Событие договорённости о доставке."""

    type: Literal[WebhookType.DELIV_AGREEMENT] = WebhookType.DELIV_AGREEMENT
    attributes: DelivAgreementAttributes


class CourierInfoEvent(WebhookEventBase):
    """Событие с информацией о курьере."""

    type: Literal[WebhookType.COURIER_INFO] = WebhookType.COURIER_INFO
    attributes: CourierInfoAttributes


class ReceiptEvent(WebhookEventBase):
    """Событие чека (атрибуты слабо типизированы)."""

    type: Literal[WebhookType.RECEIPT] = WebhookType.RECEIPT
    attributes: ReceiptAttributes = Field(default_factory=ReceiptAttributes)


WebhookEvent = Annotated[
    OrderStatusEvent
    | OrderModifiedEvent
    | PrintFormEvent
    | DownloadPhotoEvent
    | PrealertClosedEvent
    | AccompanyingWaybillEvent
    | OfficeAvailabilityEvent
    | DelivProblemEvent
    | DelivAgreementEvent
    | CourierInfoEvent
    | ReceiptEvent,
    Field(discriminator="type"),
]

_webhook_event_adapter: TypeAdapter[WebhookEvent] = TypeAdapter(WebhookEvent)


def parse_webhook(payload: dict[str, Any] | str | bytes) -> WebhookEvent:
    """
    Разобрать входящий webhook CDEK в типизированную модель.

    Args:
        payload: JSON dict, строка или bytes тела запроса.

    Returns:
        Экземпляр одного из типов WebhookEvent.
    """
    if isinstance(payload, bytes):
        payload = payload.decode("utf-8")
    if isinstance(payload, str):
        payload = json.loads(payload)
    return _webhook_event_adapter.validate_python(payload)
