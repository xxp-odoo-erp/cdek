from ..app import App
from .filters import CheckFilter
from .responses import CheckResponse


class CheckApp(App):
    filter = CheckFilter

    def get(self, filter_params: CheckFilter):
        """
        Метод используется для получения информации
        о чеке по заказу или за выбранный день
        """
        if not isinstance(filter_params, CheckFilter):
            raise ValueError("filter_params must be a CheckFilter")
        response = self._api_request(
            "GET", "check", filter_params.model_dump(exclude_none=True)
        )
        return CheckResponse.model_validate(response)
