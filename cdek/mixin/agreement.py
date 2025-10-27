from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..entity.requests.location import Location

@dataclass
class Agreement:
    """Trait для работы с согласованными данными доставки"""

    date: str | None = None
    time_from: str | None = None
    time_to: str | None = None
    delivery_point: str | None = None
    to_location: 'Location | None' = None


    def set_date(self, date: str):
        """
        Установить дату доставки, согласованную с получателем

        Args:
            date: Дата в формате 'Y-m-d', пример: 2001-02-03
        """
        self.date = date
        return self

    def set_time_from(self, time_from: str):
        """
        Установить время доставки С, согласованное с получателем

        Args:
            time_from: Время в формате ISO 8601: hh:mm, пример: 18:15
        """
        self.time_from = time_from
        return self

    def set_time_to(self, time_to: str):
        """
        Установить время доставки ПО, согласованное с получателем

        Args:
            time_to: Время в формате ISO 8601: hh:mm, пример: 20:00
        """
        self.time_to = time_to
        return self

    def set_delivery_point(self, delivery_point: 'Location'):
        if self.to_location is not None:
            raise ValueError('Код ПВЗ delivery_point нельзя передавать одновременно с параметром Адрес доставки')

        self.delivery_point = delivery_point
        return self

    def set_to_location(self, to_location: 'Location'):
        if self.delivery_point is not None:
            raise ValueError('Адрес доставки нельзя передавать одновременно с параметром кода ПВЗ delivery_point')

        self.to_location = to_location
        return self
