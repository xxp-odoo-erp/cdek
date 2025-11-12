from ..app import App
from .filters import CheckFilter
from .responses import CheckResponse


class CheckApp(App):

    def get(self, filter_params: CheckFilter):
        """
        Метод используется для получения информации
        о чеке по заказу или за выбранный день
        """
        if not isinstance(filter_params, CheckFilter):
            raise ValueError("filter_params must be a CheckFilter")
        response = self._get("check", params=filter_params)
        return CheckResponse.model_validate(response)
