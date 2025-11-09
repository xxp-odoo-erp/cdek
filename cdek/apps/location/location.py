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

    city_filter = CityFilter
    region_filter = RegionFilter
    zip_filter = ZipFilter
    coordinates_filter = CoordinatesFilter
    city_list_filter = CityListFilter

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
            CityResponse | None: Объект CityResponse с информацией о найденном городе
            или None, если город не найден
        """
        # Обрабатываем filter_params как словарь
        if not isinstance(filter_params, CityFilter | None):
            raise ValueError("filter_params must be a CityFilter instance")
        params = filter_params.model_dump(exclude_none=True)
        response = self._api_request("GET", self.constants.CITY_URL, params)
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
        if not isinstance(filter_params, RegionFilter | None):
            raise ValueError("filter_params must be a RegionFilter instance")
        params = filter_params and filter_params.model_dump(exclude_none=True) or None
        response = self._api_request("GET", self.constants.REGIONS_URL, params)
        # Здесь должен быть импорт и создание RegionsResponse объектов
        return [RegionResponse.model_validate(region) for region in response]

    def zip(self, filter_params: ZipFilter | None = None):
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
        if not isinstance(filter_params, ZipFilter | None):
            raise ValueError("filter_params must be a ZipFilter instance")
        params = filter_params and filter_params.model_dump(exclude_none=True) or None
        response = self._api_request("GET", self.constants.ZIP_URL, params)
        return [ZipResponse.model_validate(zip_code) for zip_code in response]

    def coordinates(self, filter_params: CoordinatesFilter | None = None):
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
        if not isinstance(filter_params, CoordinatesFilter | None):
            raise ValueError("filter_params must be a CoordinatesFilter instance")
        params = filter_params and filter_params.model_dump(exclude_none=True) or None
        response = self._api_request("GET", self.constants.COORDINATES_URL, params)
        return [
            CoordinatesResponse.model_validate(coordinates) for coordinates in response
        ]

    def cities(self, filter_params: CityListFilter | None = None):
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
        if not isinstance(filter_params, CityListFilter | None):
            raise ValueError("filter_params must be a CityListFilter instance")
        params = filter_params and filter_params.model_dump(exclude_none=True) or None
        response = self._api_request("GET", self.constants.CITIES_URL, params)
        return [CitiesResponse.model_validate(city) for city in response]
