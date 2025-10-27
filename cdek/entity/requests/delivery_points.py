"""
Класс DeliveryPoints для запросов к API
"""

from dataclasses import dataclass, field
from .location import Location
from ...mixin.location import Location as LocationMixin
from ...mixin.delivery_points import DeliveryPoints as DeliveryPointsMixin
from ... import constants

@dataclass
class DeliveryPoints(Location, LocationMixin, DeliveryPointsMixin):
    """Класс для работы с ПВЗ"""

    TYPE_PVZ: str = 'PVZ'
    TYPE_ALL: str = 'ALL'
    TYPE_POSTOMAT: str = 'POSTOMAT'
    LANGUAGE_RUSSIAN: str = 'rus'
    LANGUAGE_ENGLISH: str = 'eng'
    LANGUAGE_CHINESE: str = 'zho'

    city_code: int | None = None
    type: str | None = None
    pattern: list[str] = field(default_factory=lambda: constants.DELIVERY_POINTS_FILTER)
