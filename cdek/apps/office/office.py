from ..app import App
from .filters import OfficeFilter
from .responses import OfficeResponse


class OfficeApp(App):
    filter = OfficeFilter

    def get(self, filter_params: OfficeFilter | None = None):
        """Получение списка ПВЗ СДЭК"""
        if not isinstance(filter_params, OfficeFilter | None):
            raise ValueError("filter_params must be a OfficeFilter instance")
        params = filter_params and filter_params.model_dump(exclude_none=True) or None
        response = self._api_request("GET", self.constants.DELIVERY_POINTS_URL, params)
        return [OfficeResponse.model_validate(office) for office in response]
