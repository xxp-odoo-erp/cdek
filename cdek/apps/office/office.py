from ..app import App
from .filters import OfficeFilter
from .responses import OfficeResponse


class OfficeApp(App):

    def get(self, filter_params: OfficeFilter | None = None):
        """Получение списка ПВЗ СДЭК"""
        if not isinstance(filter_params, OfficeFilter | None):
            raise ValueError("filter_params must be a OfficeFilter instance")
        response = self._get(self.constants.DELIVERY_POINTS_URL, params=filter_params)
        return [OfficeResponse.model_validate(office) for office in response]
