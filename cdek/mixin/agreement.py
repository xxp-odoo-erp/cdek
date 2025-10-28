from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..requests.location import Location

@dataclass
class AgreementMixin:
    """Mixin for working with agreed delivery data."""

    date: str | None = None
    time_from: str | None = None
    time_to: str | None = None
    delivery_point: str | None = None
    to_location: 'Location | None' = None


    def set_date(self, date: str):
        """
        Set the agreed delivery date.

        Args:
            date: Date in 'Y-m-d' format, e.g., 2001-02-03
        """
        self.date = date
        return self

    def set_time_from(self, time_from: str):
        """
        Set the agreed delivery start time.

        Args:
            time_from: Time in ISO 8601 format: hh:mm, e.g., 18:15
        """
        self.time_from = time_from
        return self

    def set_time_to(self, time_to: str):
        """
        Set the agreed delivery end time.

        Args:
            time_to: Time in ISO 8601 format: hh:mm, e.g., 20:00
        """
        self.time_to = time_to
        return self

    def set_delivery_point(self, delivery_point: 'Location'):
        """Set the pickup point code. Cannot be used together with to_location."""
        if self.to_location is not None:
            raise ValueError('delivery_point cannot be set together with to_location')

        self.delivery_point = delivery_point
        return self

    def set_to_location(self, to_location: 'Location'):
        """Set the destination location. Cannot be used together with delivery_point."""
        if self.delivery_point is not None:
            raise ValueError('to_location cannot be set together with delivery_point')

        self.to_location = to_location
        return self
