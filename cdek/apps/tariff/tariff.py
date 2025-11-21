from ..app import App
from .requests import TariffCodeRequest, TariffListRequest
from .responses import TariffAvailableResponse, TariffListResponse, TariffResponse


class TariffApp(App):
    """Класс для работы с тарифами"""

    def calc_list(self, tariff: "TariffListRequest") -> "TariffListResponse":
        """Расчёт стоимости и сроков доставки по всем доступным тарифам

        Args:
            tariff: объект Tariff с параметрами запроса
            (type, from_location, to_location, packages)

        Returns:
            Список объектов TariffListResponse с информацией о доступных тарифах

        Raises:
            ValueError: если tariff не является объектом TariffListRequest
        """
        if not isinstance(tariff, TariffListRequest):
            raise ValueError("tariff must be a TariffListRequest")
        response = self._post("calculator/tarifflist", json=tariff)
        return TariffListResponse.model_validate(response)

    def calc(self, tariff: "TariffCodeRequest") -> "TariffResponse":
        """
        Расчёт стоимости и сроков доставки по коду тарифа

        Args:
            tariff: объект TariffCodeRequest с параметрами запроса
            (tariff_code, from_location, to_location, packages)

        Returns:
            TariffResponse: объект с информацией о расчёте стоимости и сроков доставки

        Raises:
            ValueError: если tariff не является объектом TariffCodeRequest
        """
        if not isinstance(tariff, TariffCodeRequest):
            raise ValueError("tariff must be a TariffCodeRequest")
        response = self._post("calculator/tariff", json=tariff)
        return TariffResponse.model_validate(response)

    def all(self) -> "TariffAvailableResponse":
        """
        Список доступных тарифов
        Метод позволяет получить список всех доступных и актуальных тарифов по договору

        Returns:
            Список объектов TariffAvailableResponse с информацией о доступных тарифах
        """
        response = self._get("calculator/alltariffs")
        return TariffAvailableResponse.model_validate(response)
