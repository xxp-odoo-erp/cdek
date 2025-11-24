from enum import Enum


class WebhookType(str, Enum):
    """Типы вебхуков."""

    # событие по статусам
    ORDER_STATUS = "ORDER_STATUS"
    # готовность печатной формы
    ORDER_MODIFIED = "ORDER_MODIFIED"
    # получение информации о закрытии преалерта
    PRINT_FORM = "PRINT_FORM"
    #
    RECEIPT = "RECEIPT"
    DOWNLOAD_PHOTO = "DOWNLOAD_PHOTO"
    PREALERT_CLOSED = "PREALERT_CLOSED"
    ACCOMPANYING_WAYBILL = "ACCOMPANYING_WAYBILL"
    OFFICE_AVAILABILITY = "OFFICE_AVAILABILITY"
    DELIV_PROBLEM = "DELIV_PROBLEM"
    DELIV_AGREEMENT = "DELIV_AGREEMENT"
