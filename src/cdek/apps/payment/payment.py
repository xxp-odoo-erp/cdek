from datetime import date as Date

from ..app import App
from .responses import PaymentInfoResponse, PaymentResponse


class PaymentApp(App):
    """Класс для работы с переводами наложенного платежа"""

    def get(self, date: Date) -> PaymentInfoResponse:
        """
        Запрос на получение информации о переводе наложенного платежа

        Args:
            date: дата для получения информации о переводе наложенного платежа

        Returns:
            PaymentInfoResponse: объект с информацией о переводе наложенного платежа

        Raises:
            ValueError: если date не является объектом Date
        """
        if not isinstance(date, Date):
            raise ValueError("date must be a Date")
        formatted_date_string = date.strftime("%Y-%m-%d")
        response = self._get("payment", params={"date": formatted_date_string})
        return PaymentInfoResponse.model_validate(response)

    def get_registries(self, date: Date) -> PaymentResponse:
        """
        Получение информации о реестрах НП

        Args:
            date: дата для получения информации о реестрах НП

        Returns:
            PaymentResponse: объект с информацией о реестрах НП

        Raises:
            ValueError: если date не является объектом Date
        """
        if not isinstance(date, Date):
            raise ValueError("date must be a Date")
        formatted_date_string = date.strftime("%Y-%m-%d")
        response = self._get("registries", params={"date": formatted_date_string})
        return PaymentResponse.model_validate(response)
