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
        """
        if not isinstance(tariff, TariffListRequest):
            raise ValueError("tariff должен быть объектом TariffListRequest")
        response = self._post(self.constants.CALC_TARIFFLIST_URL, json=tariff)
        return TariffListResponse.model_validate(response)

    def calc(self, tariff: "TariffCodeRequest") -> "TariffResponse":
        """Расчёт стоимости и сроков доставки по коду тарифа"""
        if not isinstance(tariff, TariffCodeRequest):
            raise ValueError("tariff должен быть объектом TariffCodeRequest")
        response = self._post(self.constants.CALC_TARIFF_URL, json=tariff)
        return TariffResponse.model_validate(response)

    def all(self) -> "TariffAvailableResponse":
        """
        Список доступных тарифов
        Метод позволяет получить список всех доступных и актуальных тарифов по договору

        Returns:
            Список объектов TariffAvailableResponse с информацией о доступных тарифах
        """
        response = self._get(self.constants.CALC_ALLTARIFFS_URL)
        return TariffAvailableResponse.model_validate(response)
