from __future__ import annotations

from datetime import date as Date
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, field_serializer

from .contact import Contact
from .location import OrderLocation
from .money import Money, Vat
from .package import Package
from .payment_info import PaymentInfo
from .seller import Seller


class AccompanyingWaybill(BaseModel):
    client_name: str = Field(
        ..., description="Наименование юрлица клиента, создающего СНТ"
    )
    flight_number: Optional[str] = Field(None, description="Номер рейса")
    air_waybill_numbers: Optional[list[str]] = Field(
        None, description="Накладные перевозчика для авиарейса"
    )
    vehicle_numbers: Optional[list[str]] = Field(None, description="Номера автомобилей")
    vehicle_driver: Optional[str] = Field(None, description="Водитель автомобиля")
    planned_departure_date_time: Optional[datetime] = Field(
        None, description="Планируемая дата отправления"
    )

    @field_serializer("planned_departure_date_time")
    def serialize_planned_departure_date_time(
        self, planned_departure_date_time: datetime
    ) -> str:
        """Преобразовать дату отправления СНТ в строку ISO 8601"""
        return planned_departure_date_time.strftime("%Y-%m-%dT%H:%M:%S")


class OrderStatus(BaseModel):
    """Статус заказа."""

    code: Optional[str] = Field(None, description="Код статуса")
    name: Optional[str] = Field(None, description="Название статуса")
    date_time: Optional[datetime] = Field(
        None, description="Дата и время установки статуса"
    )
    reason_code: Optional[str] = Field(None, description="Дополнительный код статуса")
    city: Optional[str] = Field(
        None, description="Наименование места возникновения статуса"
    )
    city_uuid: Optional[str] = Field(
        None, description="Идентификатор места (города) возникновения статуса"
    )
    deleted: Optional[bool] = Field(None, description="Признак удаления статуса")

    @field_serializer("date_time")
    def serialize_date_time(self, date_time: datetime) -> str:
        """Вернуть время установки статуса в формате ISO 8601"""
        return date_time.strftime("%Y-%m-%dT%H:%M:%S")


class DeliveryDetail(BaseModel):
    date: Optional[Date] = Field(None, description="Дата доставки")
    recipient_name: Optional[str] = Field(None, description="Получатель при доставке")
    payment_sum: Optional[float] = Field(None, description="Сумма наложенного платежа")
    delivery_sum: float = Field(..., description="Сумма доставки")
    total_sum: float = Field(..., description="Общая сумма")
    payment_info: Optional[list[PaymentInfo]] = Field(
        None, description="Информация о платеже"
    )
    delivery_vat_rate: Optional[float] = Field(None, description="Ставка НДС для доставки")
    delivery_vat_sum: Optional[float] = Field(None, description="Сумма НДС для доставки")
    delivery_discount_percent: Optional[float] = Field(
        None, description="Процент скидки для доставки"
    )
    delivery_discount_sum: Optional[float] = Field(
        None, description="Сумма скидки для доставки"
    )

    @field_serializer("date")
    def serialize_date(self, date: Date) -> str:
        """Представить дату доставки в формате YYYY-MM-DD"""
        return date.strftime("%Y-%m-%d")


class DeliveryProblem(BaseModel):
    code: Optional[str] = Field(None, description="Код проблемы")
    create_date: Optional[datetime] = Field(None, description="Дата создания проблемы")

    @field_serializer("create_date")
    def serialize_create_date(self, create_date: datetime) -> str:
        """Вернуть дату создания проблемы в формате ISO 8601"""
        return create_date.strftime("%Y-%m-%dT%H:%M:%S")


class FailedCall(BaseModel):
    date_time: datetime = Field(..., description="Дата и время недозвона")
    reason_code: int = Field(..., description="Причина недозвона")

    @field_serializer("date_time")
    def serialize_date_time(self, date_time: datetime) -> str:
        """Представить дату и время недозвона в формате ISO 8601"""
        return date_time.strftime("%Y-%m-%dT%H:%M:%S")


class RescheduledCall(BaseModel):
    date_time: datetime = Field(
        ..., description="Дата и время создания переноса прозвона"
    )
    date_next: Date = Field(..., description="Дата переноса прозвона")
    time_next: str = Field(..., description="Время переноса прозвона")
    comment: Optional[str] = Field(None, description="Комментарий к переносу прозвона")

    @field_serializer("date_time")
    def serialize_date_time(self, date_time: datetime) -> str:
        """Представить дату создания переноса прозвона в формате ISO 8601"""
        return date_time.strftime("%Y-%m-%dT%H:%M:%S")

    @field_serializer("date_next")
    def serialize_date_next(self, date_next: Date) -> str:
        """Вернуть дату следующего прозвона в формате YYYY-MM-DD"""
        return date_next.strftime("%Y-%m-%d")


class Call(BaseModel):
    failed_calls: Optional[list[FailedCall]] = Field(
        None, description="Информация о неуспешных прозвонах (недозвонах)"
    )
    rescheduled_calls: Optional[list[RescheduledCall]] = Field(
        None, description="Информация о переносах прозвона"
    )


class DeliveryRecipientCost(Money):
    value: float = Field(..., description="Сумма платежа, включая НДС")


class DeliveryCostThreshold(Vat):
    threshold: Optional[int] = Field(None, description="Порог стоимости товара")
    sum: Optional[float] = Field(
        None,
        description="Доп. сбор за доставку товаров",
    )


class AdditionalService(BaseModel):
    code: str = Field(..., description="Тип дополнительной услуги")
    parameter: Optional[str] = Field(None, description="Параметр дополнительной услуги")


class UpdateOrder(BaseModel):
    type: Optional[int] = Field(None, description="Тип заказа")
    number: Optional[str] = Field(None, description="Номер заказа в ИС Клиента")
    accompanying_number: Optional[str] = Field(
        None, description="Номер сопроводительной накладной на товар (СНТ)"
    )
    tariff_code: Optional[int] = Field(None, description="Код тарифа")
    comment: Optional[str] = Field(None, description="Комментарий к заказу")
    shipment_point: Optional[str] = Field(None, description="Код ПВЗ СДЭК")
    delivery_point: Optional[str] = Field(None, description="Код ПВЗ СДЭК")
    delivery_recipient_cost: Optional[DeliveryRecipientCost] = Field(
        None, description="Стоимость доставки"
    )
    delivery_recipient_cost_adv: Optional[list[DeliveryCostThreshold]] = Field(
        None, description="Пороговая стоимость доставки"
    )
    sender: Optional[Contact] = Field(None, description="Отправитель")
    seller: Optional[Seller] = Field(None, description="Реквизиты истинного продавца")
    recipient: Contact = Field(..., description="Получатель")
    from_location: Optional[OrderLocation] = Field(None, description="Адрес отправления")
    to_location: Optional[OrderLocation] = Field(None, description="Адрес доставки")
    services: Optional[list[AdditionalService]] = Field(
        None, description="Дополнительные услуги"
    )
    packages: Optional[list[Package]] = Field(None, description="Упаковки")
    has_reverse_order: Optional[bool] = Field(
        None, description="Признак необходимости создания реверсного заказа"
    )


class Order(UpdateOrder):
    additional_order_types: Optional[list[int]] = Field(
        None, description="Дополнительные типы заказа"
    )
    tariff_code: int = Field(..., description="Код тарифа")
    date_invoice: Optional[Date] = Field(None, description="Дата инвойса")
    shipper_name: Optional[str] = Field(None, description="Грузоотправитель")
    shipper_address: Optional[str] = Field(None, description="Адрес грузоотправителя")
    services: Optional[list[AdditionalService]] = Field(
        None, description="Дополнительные услуги"
    )
    packages: list[Package] = Field(default_factory=list, description="Упаковки")
    is_client_return: Optional[bool] = Field(
        None, description="Признак клиентского возврата"
    )

    @field_serializer("date_invoice")
    def serialize_date_invoice(self, date_invoice: Date) -> str:
        """Вернуть дату инвойса в формате YYYY-MM-DD"""
        return date_invoice.strftime("%Y-%m-%d")

    @classmethod
    def location_init(cls, **kwargs) -> OrderLocation:
        """Создать объект адреса заказа с указанными полями"""
        return OrderLocation(**kwargs)

    @classmethod
    def seller_init(cls, **kwargs) -> Seller:
        """Создать объект продавца по переданным параметрам"""
        return Seller(**kwargs)

    @classmethod
    def contact_init(cls, **kwargs) -> Contact:
        """Создать объект контакта отправителя или получателя"""
        return Contact(**kwargs)

    def set_seller(self, seller: Seller):
        """Установить продавца для текущего заказа"""
        self.seller = seller
        return self

    def set_from_location(self, location: OrderLocation):
        """Задать адрес отправления"""
        self.from_location = location
        return self

    def set_to_location(self, location: OrderLocation):
        """Задать адрес доставки"""
        self.to_location = location
        return self

    def set_contact(self, sender: Contact):
        """Сохранить контактные данные отправителя"""
        self.sender = sender
        return self

    def set_recipient(self, recipient: Contact):
        """Сохранить контактные данные получателя"""
        self.recipient = recipient
        return self

    @classmethod
    def package_init(cls, **kwargs):
        """Создать объект упаковки по переданным параметрам"""
        return Package(**kwargs)

    def add_package(self, package):
        """Добавить упаковку в список пакетов заказа"""
        if self.packages is None:
            self.packages = []
        self.packages.append(package)
        return self


class OrderInfo(BaseModel):
    cdek_number: Optional[int] = Field(None, description="Номер заказа")
    order_uuid: Optional[str] = Field(None, description="Идентификатор заказа")
