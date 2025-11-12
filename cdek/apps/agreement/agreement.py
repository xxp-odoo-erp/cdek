from typing import Any

from ..app import App
from ..models.entity_response import EntityResponse
from .requests import DeliveryIntervalRequest, RegisterDeliveryRequest
from .responses import AgreementInfoResponse, AvailableDeliveryIntervalsResponse


class AgreementApp(App):

    def _get_interval(self, params: Any = None):
        """Получение интервалов доставки"""
        response = self._get(self.constants.COURIER_AGREEMENTS_INTERVALS_URL, params)
        return AvailableDeliveryIntervalsResponse.model_validate(response)

    def get_interval_number(
        self, cdek_number: str
    ) -> AvailableDeliveryIntervalsResponse:
        """Получение интервалов доставки по номеру заказа"""
        """Получение интервалов доставки"""
        return self._get_interval({"cdek_number": cdek_number})

    def get_interval_uuid(self, uuid: str) -> AvailableDeliveryIntervalsResponse:
        """Получение интервалов доставки по UUID заказа"""
        return self._get_interval({"order_uuid": uuid})

    def create(self, agreement: "RegisterDeliveryRequest"):
        """Регистрация договоренности о доставке"""
        if not isinstance(agreement, RegisterDeliveryRequest):
            raise ValueError("agreement must be a RegisterDeliveryRequest")
        response = self._post(self.constants.COURIER_AGREEMENTS_URL, json=agreement)
        return EntityResponse.model_validate(response)

    def get(self, uuid: str) -> AgreementInfoResponse:
        """Получение договоренностей для курьера"""
        response = self._get(f"{self.constants.COURIER_AGREEMENTS_URL}/{uuid}")
        return AgreementInfoResponse.model_validate(response)

    def get_intervals_before_create_order(
        self, request: "DeliveryIntervalRequest"
    ) -> AvailableDeliveryIntervalsResponse:
        """Получение интервалов доставки до создания заказа"""
        if not isinstance(request, DeliveryIntervalRequest):
            raise ValueError("request must be a DeliveryIntervalRequest")
        response = self._post(
            self.constants.COURIER_AGREEMENTS_ESTIMATE_URL, json=request
        )
        return AvailableDeliveryIntervalsResponse.model_validate(response)
