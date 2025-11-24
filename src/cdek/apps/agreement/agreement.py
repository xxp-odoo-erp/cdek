from typing import Any

from ..app import App
from ..models.entity_response import EntityResponse
from .requests import DeliveryIntervalRequest, RegisterDeliveryRequest
from .responses import AgreementInfoResponse, AvailableDeliveryIntervalsResponse


class AgreementApp(App):
    """Класс для работы с договоренностями о доставке"""

    def _get_interval(
        self, params: dict[str, Any]
    ) -> AvailableDeliveryIntervalsResponse:
        """Получение интервалов доставки

        Args:
            params (Any): параметры для получения интервалов доставки

        Returns:
            AvailableDeliveryIntervalsResponse: объект с информацией
            о интервалах доставки
        """
        response = self._get("delivery/intervals", params)
        return AvailableDeliveryIntervalsResponse.model_validate(response)

    def get_interval_number(
        self, cdek_number: str
    ) -> AvailableDeliveryIntervalsResponse:
        """Получить интервалы доставки по номеру заказа

        Args:
            cdek_number (str): номер заказа

        Returns:
            AvailableDeliveryIntervalsResponse: объект с информацией
            о интервалах доставки
        """
        return self._get_interval({"cdek_number": cdek_number})

    def get_interval_uuid(self, uuid: str) -> AvailableDeliveryIntervalsResponse:
        """Получение интервалов доставки по UUID заказа

        Args:
            uuid (str): UUID заказа

        Returns:
            AvailableDeliveryIntervalsResponse: объект с информацией
            о интервалах доставки
        """
        return self._get_interval({"order_uuid": uuid})

    def create(self, agreement: RegisterDeliveryRequest) -> EntityResponse:
        """Регистрация договоренности о доставке

        Args:
            agreement (RegisterDeliveryRequest): объект с информацией
             о договоренности о доставке

        Returns:
            EntityResponse: объект с информацией о регистрации договоренности о доставке

        Raises:
            ValueError: если agreement не является объектом RegisterDeliveryRequest
        """
        if not isinstance(agreement, RegisterDeliveryRequest):
            raise ValueError("agreement must be a RegisterDeliveryRequest")
        response = self._post("delivery", json=agreement)
        return EntityResponse.model_validate(response)

    def get(self, uuid: str) -> AgreementInfoResponse:
        """Получение договоренностей для курьера

        Args:
            uuid (str): UUID договора

        Returns:
            AgreementInfoResponse: объект с информацией о договорах
        """
        response = self._get(f"delivery/{uuid}")
        return AgreementInfoResponse.model_validate(response)

    def get_intervals_before_create_order(
        self, request: "DeliveryIntervalRequest"
    ) -> AvailableDeliveryIntervalsResponse:
        """Получение интервалов доставки до создания заказа

        Args:
            request (DeliveryIntervalRequest): объект с информацией
            о запросе на получение интервалов доставки до создания заказа

        Returns:
            AvailableDeliveryIntervalsResponse: объект с информацией о интервалах
                доставки до создания заказа

        Raises:
            ValueError: если request не является объектом DeliveryIntervalRequest
        """
        if not isinstance(request, DeliveryIntervalRequest):
            raise ValueError("request must be a DeliveryIntervalRequest")
        response = self._post("delivery/estimatedIntervals", json=request)
        return AvailableDeliveryIntervalsResponse.model_validate(response)
