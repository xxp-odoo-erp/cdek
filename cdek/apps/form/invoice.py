from ..app import App
from ..models.entity_response import EntityResponse
from .requests import PrintInvoiceRequest
from .responses import WaybillEntityResponse


class InvoiceApp(App):
    invoice = PrintInvoiceRequest

    def get(self, uuid: str):
        """Получение сущности накладной к заказу"""
        response = self._api_request("GET", f"{self.constants.INVOICE_URL}/{uuid}")
        return WaybillEntityResponse.model_validate(response)

    def get_pdf(self, uuid: str):
        """Получение PDF накладной к заказу"""
        return self._api_request("GET", f"{self.constants.INVOICE_URL}/{uuid}.pdf")

    def set(self, invoice: PrintInvoiceRequest) -> EntityResponse:
        """Запрос на формирование накладной к заказу"""
        response = self._api_request("POST", self.constants.INVOICE_URL, invoice)
        return EntityResponse.model_validate(response)
