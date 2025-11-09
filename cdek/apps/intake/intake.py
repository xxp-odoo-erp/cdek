from ..app import App
from ..models.entity_response import EntityResponse
from .filters import IntakeDateFilter, IntakeFilter
from .requests import IntakeRequest
from .responses import IntakeDateResponse, IntakeEntityResponse


class IntakeApp(App):
    call_filter = IntakeDateFilter
    intake = IntakeRequest
    filter = IntakeFilter

    def get_call_dates(self, date_request: IntakeDateFilter):
        if not isinstance(date_request, IntakeDateFilter):
            raise ValueError("date_request must be a IntakeDateRequest")
        params = date_request.model_dump(exclude_none=True)
        response = self._api_request("GET", self.constants.INTAKES_DAYS_URL, params)
        return IntakeDateResponse.model_validate(response)

    def update(self, intake: IntakeFilter):
        if not isinstance(intake, IntakeFilter):
            raise ValueError("intake must be a IntakeFilter")
        params = intake.model_dump(exclude_none=True)
        response = self._api_request("PATCH", self.constants.INTAKES_URL, params)
        return EntityResponse.model_validate(response)

    def create(self, intake: IntakeRequest):
        """Создание заявки на вызов курьера"""
        if not isinstance(intake, IntakeRequest):
            raise ValueError("intake must be a IntakeRequest")
        params = intake.model_dump(exclude_none=True)
        response = self._api_request("POST", self.constants.INTAKES_URL, params)
        return EntityResponse.model_validate(response)

    def get(self, uuid: str):
        """Информация о заявке на вызов курьера"""
        response = self._api_request("GET", f"{self.constants.INTAKES_URL}/{uuid}")
        return IntakeEntityResponse.model_validate(response)

    def delete(self, uuid: str):
        """Удаление заявки на вызов курьера"""
        response = self._api_request("DELETE", f"{self.constants.INTAKES_URL}/{uuid}")
        return EntityResponse.model_validate(response)
