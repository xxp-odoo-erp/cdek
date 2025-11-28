from ..app import App
from ..models.entity_response import EntityResponse
from .requests import OrderRequest, OrderUpdateRequest
from .responses import OrderEntityResponse


class OrderApp(App):
    """Класс для работы с заказами"""

    def create(self, order: "OrderRequest") -> "EntityResponse":
        """
        Создать заказ в системе CDEK

        Args:
            order: объект OrderRequest с параметрами запроса

        Returns:
            EntityResponse: объект с информацией о созданном заказе

        Raises:
            ValueError: если order не является объектом OrderRequest
        """
        if not isinstance(order, OrderRequest):
            raise ValueError("order must be a OrderRequest")
        response = self._post("orders", json=order)
        return EntityResponse.model_validate(response)

    def update(self, order: "OrderUpdateRequest") -> "EntityResponse":
        """
        Обновить сведения по ранее созданному заказу

        Args:
            order: объект OrderUpdateRequest с параметрами запроса

        Returns:
            EntityResponse: объект с информацией о обновленном заказе

        Raises:
            ValueError: если order не является объектом OrderUpdateRequest
        """
        if not isinstance(order, OrderUpdateRequest):
            raise ValueError("order must be a OrderUpdateRequest")
        response = self._patch("orders", json=order)
        return EntityResponse.model_validate(response)

    def delete(self, uuid: str) -> EntityResponse:
        """
        Удалить заказ по его UUID

        Args:
            uuid: идентификатор заказа

        Returns:
            EntityResponse: объект с информацией о удаленном заказе

        Raises:
            ValueError: если uuid не является строкой
        """
        if not isinstance(uuid, str):
            raise ValueError("uuid must be a str")
        response = self._delete(f"orders/{uuid}")
        return EntityResponse.model_validate(response)

    def refusal(self, uuid: str) -> EntityResponse:
        """Регастрация отказа

        Регистрации отказа по заказу и дальнейшего возврата
        данного заказа в интернет-магазин.
        После успешной регистрации отказа статус заказа переходит
        в "Не вручен" (код NOT_DELIVERED) с дополнительным
        статусом "Возврат, отказ от получения: Без объяснения" (код 11).
        Заказ может быть отменен в любом статусе*, пока не установлен статус
        "Вручен" или "Не вручен".
        * Не рекомендуется использовать метод для заказов,
        которые находятся в статусе "Создан" и не планируются к отгрузке
        на склады СДЭК. В случае применения метода отказа для заказов,
        находящихся в статусе "Создан", по ним будут начислены
        операции и заказы будут включены в Акт оказанных услуг.
        Для отмены заказа в статусе "Создан" воспользуйтесь методом
        "Удаление заказа".

        Args:
            uuid: идентификатор заказа

        Returns:
            EntityResponse: объект с информацией о регистрации отказа

        Raises:
            ValueError: если uuid не является строкой
        """
        if not isinstance(uuid, str):
            raise ValueError("uuid must be a str")
        response = self._post(f"orders/{uuid}/refusal")
        return EntityResponse.model_validate(response)

    def client_return(self, uuid: str, tariff_code: int) -> "EntityResponse":
        """Регистрация клиентского возврата

        Args:
            uuid: идентификатор заказа
            tariff_code: код тарифа

        Returns:
            EntityResponse: объект с информацией о регистрации клиентского возврата
        """
        response = self._post(
            f"orders/{uuid}/clientReturn",
            json={"tariff_code": tariff_code},
        )
        return EntityResponse.model_validate(response)

    def get_by_cdek_number(self, cdek_number: str) -> "OrderEntityResponse":
        """Полная информация о заказе по трек номеру

        Args:
            cdek_number: трек номер заказа

        Returns:
            OrderEntityResponse: объект с информацией о заказе
        """
        response = self._get("orders", params={"cdek_number": cdek_number})
        return OrderEntityResponse.model_validate(response)

    def get_by_im_number(self, im_number: str) -> OrderEntityResponse:
        """Полная информация о заказе по ID заказа в магазине

        Args:
            im_number: ID заказа в магазине

        Returns:
            OrderEntityResponse: объект с информацией о заказе
        """
        response = self._get("orders", params={"im_number": im_number})
        return OrderEntityResponse.model_validate(response)

    def get_by_uuid(self, uuid: str) -> OrderEntityResponse:
        """Полная информация о заказе по uuid

        Args:
            uuid: идентификатор заказа

        Returns:
            OrderEntityResponse: объект с информацией о заказе
        """
        response = self._get(f"orders/{uuid}")
        return OrderEntityResponse.model_validate(response)
