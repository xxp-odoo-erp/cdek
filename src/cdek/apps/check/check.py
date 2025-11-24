from ..app import App
from .filters import CheckFilter
from .responses import CheckResponse


class CheckApp(App):
    """Класс для работы с чеками"""

    def get(self, filter_params: CheckFilter) -> CheckResponse:
        """
        Метод используется для получения информации
        о чеке по заказу или за выбранный день

        Args:
            filter_params (CheckFilter): фильтр для получения
                информации о чеке по заказу или за выбранный день

        Returns:
            CheckResponse: объект с информацией о чеке по заказу или за выбранный день

        Raises:
            ValueError: если filter_params не является объектом CheckFilter
        """
        if not isinstance(filter_params, CheckFilter):
            raise ValueError("filter_params must be a CheckFilter")
        response = self._get("check", params=filter_params)
        return CheckResponse.model_validate(response)
