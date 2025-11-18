from ..app import App
from .filters import OfficeFilter
from .responses import OfficeResponse


class OfficeApp(App):
    """Класс для работы с ПВЗ СДЭК"""

    def get(self, filter_params: OfficeFilter | None = None):
        """Получение списка ПВЗ СДЭК

        Args:
            filter_params (OfficeFilter): фильтр для получения списка ПВЗ СДЭК

        Returns:
            list[OfficeResponse]: список объектов OfficeResponse с информацией о ПВЗ

        Raises:
            ValueError: если filter_params не является объектом OfficeFilter
        """
        if not isinstance(filter_params, OfficeFilter | None):
            raise ValueError("filter_params must be a OfficeFilter instance")
        response = self._get("deliverypoints", params=filter_params)
        return [OfficeResponse.model_validate(office) for office in response]
