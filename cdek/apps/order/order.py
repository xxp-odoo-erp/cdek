from ..app import App
from ..models.entity_response import EntityResponse
from .requests import OrderRequest, OrderUpdateRequest
from .responses import OrderEntityResponse


class OrderApp(App):
    order = OrderRequest
    update_order = OrderUpdateRequest

    def create(self, order: "OrderRequest") -> "EntityResponse":
        if not isinstance(order, OrderRequest):
            raise ValueError("order must be a OrderRequest")
        response = self._api_request("POST", self.constants.ORDERS_URL, order)
        return EntityResponse.model_validate(response)

    def update(self, order: "OrderUpdateRequest") -> "EntityResponse":
        if not isinstance(order, OrderUpdateRequest):
            raise ValueError("order must be a OrderUpdateRequest")
        response = self._api_request("PATCH", self.constants.ORDERS_URL, order)
        return EntityResponse.model_validate(response)

    def delete(self, uuid: str) -> EntityResponse:
        response = self._api_request("DELETE", f"{self.constants.ORDERS_URL}/{uuid}")
        return EntityResponse.model_validate(response)

    def client_return(self, uuid: str, tariff_code: int) -> "EntityResponse":
        """Регистрация клиентского возврата"""
        response = self._api_request(
            "POST",
            f"{self.constants.ORDERS_URL}/{uuid}/clientReturn",
            {"tariff_code": tariff_code},
        )
        return EntityResponse.model_validate(response)

    def get_by_cdek_number(self, cdek_number: str) -> "OrderEntityResponse":
        """Полная информация о заказе по трек номеру"""
        response = self._api_request(
            "GET", self.constants.ORDERS_URL, {"cdek_number": cdek_number}
        )
        return OrderEntityResponse.model_validate(response)

    def get_by_im_number(self, im_number: str):
        """Полная информация о заказе по ID заказа в магазине"""
        response = self._api_request(
            "GET", self.constants.ORDERS_URL, {"im_number": im_number}
        )
        return OrderEntityResponse.model_validate(response)

    def get_by_uuid(self, uuid: str):
        """Полная информация о заказе по uuid"""
        response = self._api_request("GET", f"{self.constants.ORDERS_URL}/{uuid}")
        return OrderEntityResponse.model_validate(response)
