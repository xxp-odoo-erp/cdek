from ..app import App
from ..models.entity_response import EntityResponse
from .requests import PrintInvoiceRequest
from .responses import WaybillEntityResponse


class InvoiceApp(App):
    """Класс для работы с накладными к заказу"""

    def get(self, uuid: str) -> WaybillEntityResponse:
        """Получение сущности накладной к заказу

        Args:
            uuid (str): идентификатор накладной к заказу

        Returns:
            WaybillEntityResponse: объект с информацией о накладной к заказу
        """
        response = self._get(f"print/orders/{uuid}")
        return WaybillEntityResponse.model_validate(response)

    def get_pdf(self, uuid: str) -> bytes:
        """Получение PDF накладной к заказу

        Args:
            uuid (str): идентификатор накладной к заказу

        Returns:
            bytes: содержимое PDF файла
        """
        return self._get(f"print/orders/{uuid}.pdf")

    def set(self, invoice: PrintInvoiceRequest) -> EntityResponse:
        """Запрос на формирование накладной к заказу

        Args:
            invoice (PrintInvoiceRequest): объект с информацией о запросе
                на формирование накладной к заказу

        Returns:
            EntityResponse: объект с информацией о формировании накладной к заказу

        Raises:
            ValueError: если invoice не является объектом PrintInvoiceRequest
        """
        if not isinstance(invoice, PrintInvoiceRequest):
            raise ValueError("invoice must be a PrintInvoiceRequest")
        response = self._post("print/orders", json=invoice)
        return EntityResponse.model_validate(response)
