
from ..app import App
from .requests import DeliveryIntervalRequest, RegisterDeliveryRequest
from .responses import AgreementInfoResponse, AvailableDeliveryIntervalsResponse
from ..models.entity_response import EntityResponse


class AgreementApp(App):

    register = RegisterDeliveryRequest
    interval = DeliveryIntervalRequest
    
    def _get_interval(self, params: dict | None = None):
        """Получение интервалов доставки"""
        response = self._api_request("GET", self.constants.COURIER_AGREEMENTS_INTERVALS_URL, params)
        return AvailableDeliveryIntervalsResponse.model_validate(response)

    def get_interval_number(self, cdek_number: str):
        """Получение интервалов доставки по номеру заказа"""
        """Получение интервалов доставки"""
        return self._get_interval({"cdek_number": cdek_number})

    def get_interval_uuid(self, uuid: str):
        """Получение интервалов доставки по UUID заказа"""
        return self._get_interval({"order_uuid": uuid})

    def create(self, agreement: "RegisterDeliveryRequest"):
        """Регистрация договоренности о доставке"""
        if not isinstance(agreement, RegisterDeliveryRequest):
            raise ValueError("agreement must be a RegisterDeliveryRequest")
        params = agreement.model_dump(exclude_none=True)
        response = self._api_request("POST", self.constants.COURIER_AGREEMENTS_URL, params)
        return EntityResponse.model_validate(response)

    def get(self, uuid: str):
        """Получение договоренностей для курьера"""
        response = self._api_request("GET", f"{self.constants.COURIER_AGREEMENTS_URL}/{uuid}")
        return AgreementInfoResponse.model_validate(response)

    def get_intervals_before_create_order(self, request: "DeliveryIntervalRequest"):
        """Получение интервалов доставки до создания заказа"""
        if not isinstance(request, DeliveryIntervalRequest):
            raise ValueError("request must be a DeliveryIntervalRequest")
        params = request.model_dump(exclude_none=True)
        response = self._api_request("POST", self.constants.COURIER_AGREEMENTS_ESTIMATE_URL, params)
        return AvailableDeliveryIntervalsResponse.model_validate(response)
