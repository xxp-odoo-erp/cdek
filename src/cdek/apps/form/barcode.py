from ..app import App
from ..models.entity_response import EntityResponse
from .requests import PrintBarcodeRequest
from .responses import PrintBarcodeResponse


class BarcodeApp(App):
    """Класс для работы с ШК-местами к заказу"""

    def set(self, barcode: PrintBarcodeRequest) -> EntityResponse:
        """Запрос на формирование ШК-места к заказу

        Args:
            barcode (PrintBarcodeRequest): объект с информацией о запросе
                на формирование ШК-места к заказу

        Returns:
            EntityResponse: объект с информацией о формировании ШК-места к заказу

        Raises:
            ValueError: если barcode не является объектом PrintBarcodeRequest
        """
        if not isinstance(barcode, PrintBarcodeRequest):
            raise ValueError("barcode must be a PrintBarcodeRequest")
        response = self._post("print/barcodes", json=barcode)
        return EntityResponse.model_validate(response)

    def get(self, uuid: str) -> PrintBarcodeResponse:
        """Получение сущности ШК к заказу

        Args:
            uuid (str): идентификатор ШК-места к заказу

        Returns:
            PrintBarcodeResponse: объект с информацией о ШК-месте к заказу
        """
        response = self._get(f"print/barcodes/{uuid}")
        return PrintBarcodeResponse.model_validate(response)

    def get_pdf(self, uuid: str) -> bytes:
        """Скачивание готового ШК

        Args:
            uuid (str): идентификатор ШК-места к заказу

        Returns:
            bytes: содержимое PDF файла
        """
        return self._get(f"print/barcodes/{uuid}.pdf")
