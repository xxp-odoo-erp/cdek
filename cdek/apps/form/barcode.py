from ..app import App
from ..models.entity_response import EntityResponse
from .requests import PrintBarcodeRequest
from .responses import PrintBarcodeResponse


class BarcodeApp(App):
    barcode = PrintBarcodeRequest

    def set(self, barcode: PrintBarcodeRequest):
        """Запрос на формирование ШК-места к заказу"""
        response = self._post(self.constants.BARCODES_URL, json=barcode)
        return EntityResponse.model_validate(response)

    def get(self, uuid: str) -> PrintBarcodeResponse:
        """Получение сущности ШК к заказу"""
        response = self._get(f"{self.constants.BARCODES_URL}/{uuid}")
        return PrintBarcodeResponse.model_validate(response)

    def get_pdf(self, uuid: str):
        """Скачивание готового ШК"""
        return self._get(f"{self.constants.BARCODES_URL}/{uuid}.pdf")
