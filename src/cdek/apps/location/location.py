from __future__ import annotations

from ..app import App
from .filters import (
    CityFilter,
    CityListFilter,
    CoordinatesFilter,
    RegionFilter,
    ZipFilter,
)
from .responses import (
    CitiesResponse,
    CityResponse,
    CoordinatesResponse,
    RegionResponse,
    ZipResponse,
)


class LocationApp(App):
    """Получение списка локаций"""

    def city(self, filter_params: CityFilter) -> CityResponse | None:
        """
        Подбор локации по названию города
        Метод позволяет получать подсказки по подбору населенного пункта
        по его наименованию.

        Args:
            filter_params (CityFilter): Фильтр для подбора города

        Raises:
            ValueError: Если filter_params не является объектом CityFilter

        Returns:
            Optional[CityResponse]: Объект CityResponse с информацией о найденном городе
            или None, если город не найден
        """
        # Обрабатываем filter_params как словарь
        if filter_params is not None and not isinstance(filter_params, CityFilter):
            raise ValueError("filter_params must be a CityFilter instance")
        response = self._get("location/suggest/cities", params=filter_params)
        return CityResponse.model_validate(response) if response else None

    def regions(
        self, filter_params: RegionFilter | None = None
    ) -> list[RegionResponse]:
        """
        Получение списка регионов
        Метод предназначен для получения детальной информации о регионах.

        Args:
            filter_params (RegionFilter): Фильтр для получения списка регионов

        Raises:
            ValueError: Если filter_params не является объектом RegionFilter

        Returns:
            list[RegionResponse]: Список объектов RegionResponse
            с информацией о регионах
        """
        if filter_params is not None and not isinstance(filter_params, RegionFilter):
            raise ValueError("filter_params must be a RegionFilter instance")
        response = self._get("location/regions", params=filter_params)
        # Здесь должен быть импорт и создание RegionsResponse объектов
        return [RegionResponse.model_validate(region) for region in response]

    def zip(self, filter_params: ZipFilter | None = None) -> list[ZipResponse]:
        """
        Получение почтовых индексов города
        Метод предназначен для получения списка почтовых индексов.

        Args:
            filter_params (ZipFilter): Фильтр для получения списка почтовых индексов

        Raises:
            ValueError: Если filter_params не является объектом ZipFilter

        Returns:
            list[ZipResponse]: Список объектов ZipResponse с информацией
            о почтовых индексах
        """
        if filter_params is not None and not isinstance(filter_params, ZipFilter):
            raise ValueError("filter_params must be a ZipFilter instance")
        response = self._get("location/postalcodes", params=filter_params)
        return [ZipResponse.model_validate(zip_code) for zip_code in response]

    def coordinates(
        self, filter_params: CoordinatesFilter | None = None
    ) -> list[CoordinatesResponse]:
        """
        Получение локации по координатам
        Метод позволяет определить локацию по переданным в запросе координатам

        Args:
            filter_params (CoordinatesFilter): Фильтр
            для получения локации по координатам

        Raises:
            ValueError: Если filter_params не является объектом CoordinatesFilter

        Returns:
            list[CoordinatesResponse]: Список объектов CoordinatesResponse
            с информацией о локации
        """
        if filter_params is not None and not isinstance(
            filter_params, CoordinatesFilter
        ):
            raise ValueError("filter_params must be a CoordinatesFilter instance")
        response = self._get("location/coordinates", params=filter_params)
        return [
            CoordinatesResponse.model_validate(coordinates) for coordinates in response
        ]

    def cities(
        self, filter_params: CityListFilter | None = None
    ) -> list[CitiesResponse]:
        """
        Получение списка населенных пунктов
        Метод предназначен для получения детальной информации о населенных пунктах

        Args:
            filter_params (CityListFilter): Фильтр для получения списка городов

        Raises:
            ValueError: Если filter_params не является объектом CityListFilter

        Returns:
            list[CitiesResponse]: Список объектов CitiesResponse с информацией о городах
        """
        if filter_params is not None and not isinstance(filter_params, CityListFilter):
            raise ValueError("filter_params must be a CityListFilter instance")
        response = self._get("location/cities", params=filter_params)
        return [CitiesResponse.model_validate(city) for city in response]
