from enum import Enum


class WebhookType(str, Enum):
    """Типы вебхуков."""

    ORDER_STATUS = "ORDER_STATUS"
    ORDER_MODIFIED = "ORDER_MODIFIED"
    PRINT_FORM = "PRINT_FORM"
    RECEIPT = "RECEIPT"
    DOWNLOAD_PHOTO = "DOWNLOAD_PHOTO"
    PREALERT_CLOSED = "PREALERT_CLOSED"
    ACCOMPANYING_WAYBILL = "ACCOMPANYING_WAYBILL"
    OFFICE_AVAILABILITY = "OFFICE_AVAILABILITY"
    DELIV_PROBLEM = "DELIV_PROBLEM"
    DELIV_AGREEMENT = "DELIV_AGREEMENT"
    COURIER_INFO = "COURIER_INFO"


class PrintFormType(str, Enum):
    """Тип печатной формы в событии PRINT_FORM."""

    WAYBILL = "WAYBILL"
    BARCODE = "BARCODE"


class OfficeAvailabilityType(str, Enum):
    """Тип изменения доступности офиса."""

    AVAILABLE_OFFICE = "AVAILABLE_OFFICE"
    UNAVAILABLE_OFFICE = "UNAVAILABLE_OFFICE"


class ModificationType(str, Enum):
    """Тип изменения заказа в событии ORDER_MODIFIED."""

    PLANED_DELIVERY_DATE_CHANGED = "PLANED_DELIVERY_DATE_CHANGED"
    DELIVERY_SUM_CHANGED = "DELIVERY_SUM_CHANGED"
    DELIVERY_MODE_CHANGED = "DELIVERY_MODE_CHANGED"


class ModificationValueType(str, Enum):
    """Тип значения в new_value события ORDER_MODIFIED."""

    DATE = "DATE"
    FLOAT = "FLOAT"
    INTEGER = "INTEGER"


class DelivAgreementType(str, Enum):
    """Тип договорённости о доставке."""

    DOOR = "DOOR"
    WAREHOUSE = "WAREHOUSE"
    POSTAMAT = "POSTAMAT"


class DelivAgreementSource(str, Enum):
    """Источник договорённости о доставке."""

    DAILY_CALL_TASK = "DAILY_CALL_TASK"
    COURIER_SUPPORT = "COURIER_SUPPORT"
    EK5_INTEGRATION = "EK5_INTEGRATION"
    WEB_SITE = "WEB_SITE"
    MOBILE_APPLICATION = "MOBILE_APPLICATION"
    SELF_CARE = "SELF_CARE"
    CABINET = "CABINET"
    MIA_BOT = "MIA_BOT"
    WEB_SITE_BOT = "WEB_SITE_BOT"
    MESSENGER_BOT = "MESSENGER_BOT"


class WebhookRelatedEntityType(str, Enum):
    """Тип связанной сущности во входящем ORDER_STATUS."""

    DIRECT_ORDER = "direct_order"
    CLIENT_DIRECT_ORDER = "client_direct_order"


class CourierTaskType(str, Enum):
    """Тип задачи курьера в событии COURIER_INFO."""

    DELIVERY = "DELIVERY"
    INTAKE = "INTAKE"
