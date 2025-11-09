from enum import StrEnum, auto


class WebhookType(StrEnum):
    """Типы вебхуков."""

    # событие по статусам
    ORDER_STATUS = auto()
    # готовность печатной формы
    ORDER_MODIFIED = auto()
    # получение информации о закрытии преалерта
    PRINT_FORM = auto()
    #
    RECEIPT = auto()
    DOWNLOAD_PHOTO = auto()
    PREALERT_CLOSED = auto()
    ACCOMPANYING_WAYBILL = auto()
    OFFICE_AVAILABILITY = auto()
    DELIV_PROBLEM = auto()
    DELIV_AGREEMENT = auto()
