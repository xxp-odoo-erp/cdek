from __future__ import annotations

from ..app import App
from .filters import OfficeFilter
from .responses import OfficeResponse


class OfficeApp(App):
    """Класс для работы с ПВЗ СДЭК"""

    @property
    def headers(self) -> dict[str, str]:
        return {
            key: value
            for key, value in self._response_headers.items()
            if key.startswith("X-")
        }

    def _get_offices(
        self, filter_params: OfficeFilter | None = None
    ) -> list[OfficeResponse]:
        """Получение списка ПВЗ СДЭК

        Args:
            filter_params (OfficeFilter): фильтр для получения списка ПВЗ СДЭК

        Returns:
            list[OfficeResponse]: список объектов OfficeResponse с информацией о ПВЗ

        Raises:
            ValueError: если filter_params не является объектом OfficeFilter
        """
        if filter_params is not None and not isinstance(filter_params, OfficeFilter):
            raise ValueError("filter_params must be a OfficeFilter instance")
        response = self._get("deliverypoints", params=filter_params)
        return [OfficeResponse.model_validate(office) for office in response]

    def get(
        self, filter_params: OfficeFilter | None = None
    ) -> dict[str, list[OfficeResponse] | dict]:  # type: ignore
        """Получение списка ПВЗ СДЭК

        Args:
            filter_params (OfficeFilter): фильтр для получения списка ПВЗ СДЭК

        Returns:
            list[OfficeResponse]: список объектов OfficeResponse с информацией о ПВЗ
            dict: заголовки ответа
        """
        return {"result": self._get_offices(filter_params), "headers": self.headers}
