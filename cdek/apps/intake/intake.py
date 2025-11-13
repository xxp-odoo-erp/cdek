from ..app import App
from ..models.entity_response import EntityResponse
from .filters import IntakeDateFilter, IntakeFilter
from .requests import IntakeRequest
from .responses import IntakeDateResponse, IntakeEntityResponse


class IntakeApp(App):
    def get_call_dates(self, date_request: IntakeDateFilter):
        """Получить доступные даты вызова курьера"""
        if not isinstance(date_request, IntakeDateFilter):
            raise ValueError("date_request must be a IntakeDateRequest")
        response = self._get(self.constants.INTAKES_DAYS_URL, params=date_request)
        return IntakeDateResponse.model_validate(response)

    def update(self, intake: IntakeFilter):
        """Изменить параметры существующей заявки"""
        if not isinstance(intake, IntakeFilter):
            raise ValueError("intake must be a IntakeFilter")
        response = self._patch(self.constants.INTAKES_URL, json=intake)
        return EntityResponse.model_validate(response)

    def create(self, intake: IntakeRequest):
        """Создание заявки на вызов курьера"""
        if not isinstance(intake, IntakeRequest):
            raise ValueError("intake must be a IntakeRequest")
        response = self._post(self.constants.INTAKES_URL, json=intake)
        return EntityResponse.model_validate(response)

    def get(self, uuid: str):
        """Информация о заявке на вызов курьера"""
        response = self._get(f"{self.constants.INTAKES_URL}/{uuid}")
        return IntakeEntityResponse.model_validate(response)

    def delete(self, uuid: str):
        """Удаление заявки на вызов курьера"""
        response = self._delete(f"{self.constants.INTAKES_URL}/{uuid}")
        return EntityResponse.model_validate(response)
