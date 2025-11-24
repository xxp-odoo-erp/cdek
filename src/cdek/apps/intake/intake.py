from ..app import App
from ..models.entity_response import EntityResponse
from .filters import IntakeDateFilter, IntakeFilter
from .requests import IntakeRequest
from .responses import IntakeDateResponse, IntakeEntityResponse


class IntakeApp(App):
    """Класс для работы с заявками на вызов курьера"""

    def get_call_dates(self, date_request: IntakeDateFilter) -> IntakeDateResponse:
        """Получить доступные даты вызова курьера

        Args:
            date_request (IntakeDateFilter): фильтр для получения
                доступных дат вызова курьера

        Returns:
            IntakeDateResponse: объект с информацией о доступных датах вызова курьера

        Raises:
            ValueError: если date_request не является объектом IntakeDateFilter
        """
        if not isinstance(date_request, IntakeDateFilter):
            raise ValueError("date_request must be a IntakeDateRequest")
        response = self._get("intakes/availableDays", params=date_request)
        return IntakeDateResponse.model_validate(response)

    def update(self, intake: IntakeFilter) -> EntityResponse:
        """Изменить параметры существующей заявки

        Args:
            intake (IntakeFilter): фильтр для изменения параметров существующей заявки

        Returns:
            EntityResponse: объект с информацией о измененной заявке

        Raises:
            ValueError: если intake не является объектом IntakeFilter
        """
        if not isinstance(intake, IntakeFilter):
            raise ValueError("intake must be a IntakeFilter")
        response = self._patch("intakes", json=intake)
        return EntityResponse.model_validate(response)

    def create(self, intake: IntakeRequest) -> EntityResponse:
        """Создание заявки на вызов курьера

        Args:
            intake (IntakeRequest): объект с информацией о заявке на вызов курьера

        Returns:
            EntityResponse: объект с информацией о созданной заявке

        Raises:
            ValueError: если intake не является объектом IntakeRequest
        """
        if not isinstance(intake, IntakeRequest):
            raise ValueError("intake must be a IntakeRequest")
        response = self._post("intakes", json=intake)
        return EntityResponse.model_validate(response)

    def get(self, uuid: str) -> IntakeEntityResponse:
        """Информация о заявке на вызов курьера

        Args:
            uuid (str): идентификатор заявки на вызов курьера

        Returns:
            IntakeEntityResponse: объект с информацией о заявке на вызов курьера
        """
        response = self._get(f"intakes/{uuid}")
        return IntakeEntityResponse.model_validate(response)

    def delete(self, uuid: str) -> EntityResponse:
        """Удаление заявки на вызов курьера

        Args:
            uuid (str): идентификатор заявки на вызов курьера

        Returns:
            EntityResponse: объект с информацией о удаленной заявке
        """
        response = self._delete(f"intakes/{uuid}")
        return EntityResponse.model_validate(response)
