"""
Класс Order для запросов к API
"""

from dataclasses import dataclass
from .location import Location
from .contact import Contact
from .money import Money
from .source import Source
from ...mixin.order import Order as OrderMixin
from ...mixin.common import Common as CommonMixin
from ...mixin.tariff import Tariff as TariffMixin

@dataclass
class Order(Source, OrderMixin, CommonMixin, TariffMixin):
    """Класс для создания заказа"""

    date_invoice: str | None = None
    print: str | None = None


    def set_number(self, number: str):
        """Установить номер заказа"""
        self.number = number
        return self

    def set_shipment_point(self, shipment_point: str):
        """Установить код ПВЗ для забора"""
        self.shipment_point = shipment_point
        return self

    def set_delivery_point(self, delivery_point: str):
        """Установить код ПВЗ для доставки"""
        self.delivery_point = delivery_point
        return self

    def set_items_cost_currency(self, items_cost_currency: str):
        """Установить валюту объявленной стоимости"""
        self.items_cost_currency = items_cost_currency
        return self

    def set_recipient_currency(self, recipient_currency: str):
        """Установить валюту наложенного платежа"""
        self.recipient_currency = recipient_currency
        return self

    def set_shipment_address(self, address: str):
        """Экспресс-метод: установить адрес отправления"""
        if self.from_location is None:
            self.from_location = Location.with_address(address)
        else:
            self.from_location.set_address(address)
        return self

    def set_shipment_city_code(self, code: int):
        """Экспресс-метод: установить код города отправления"""
        if self.from_location is None:
            self.from_location = Location.with_code(code)
        else:
            self.from_location.set_code(code)
        return self

    def set_sender_city_code(self, code: int):
        """Экспресс-метод: установить код города отправителя"""
        if self.from_location is None:
            self.from_location = Location.with_code(code)
        else:
            self.from_location.set_code(code)
        return self

    def set_recipient_address(self, address: str):
        """Экспресс-метод: установить адрес получателя"""
        if self.to_location is None:
            self.to_location = Location.with_address(address)
        else:
            self.to_location.set_address(address)
        return self

    def set_recipient_city_code(self, code: int):
        """Экспресс-метод: установить код города получателя"""
        if self.to_location is None:
            self.to_location = Location.with_code(code)
        else:
            self.to_location.set_code(code)
        return self

    def set_date_invoice(self, date_invoice: str):
        """Установить дату инвойса"""
        self.date_invoice = date_invoice
        return self

    def set_shipper_name(self, shipper_name: str):
        """Установить грузоотправителя"""
        self.shipper_name = shipper_name
        return self

    def set_shipper_address(self, shipper_address: str):
        """Установить адрес грузоотправителя"""
        self.shipper_address = shipper_address
        return self

    def set_delivery_recipient_cost(self, value: float = 0.0, vat_sum=None, vat_rate=None):
        """Установить стоимость доставки"""
        args = {'value': value}
        if vat_sum is not None:
            args['vat_sum'] = vat_sum
        if vat_rate is not None:
            args['vat_rate'] = vat_rate
        self.delivery_recipient_cost = Money.express(args)
        return self

    def set_delivery_recipient_cost_adv(self, threshold, sum_val, vat_sum=None, vat_rate=None):
        """Установить пороговую стоимость доставки"""
        from .threshold import Threshold
        args = {'threshold': threshold, 'sum': sum_val}
        if vat_sum is not None:
            args['vat_sum'] = vat_sum
        if vat_rate is not None:
            args['vat_rate'] = vat_rate
        if threshold:
            self.delivery_recipient_cost_adv = Threshold.express(args)
        return self

    def set_sender(self, sender: Contact):
        """Установить отправителя"""
        self.sender = sender
        return self

    def set_seller(self, seller):
        """Установить продавца"""
        self.seller = seller
        return self

    def set_recipient(self, recipient: Contact):
        """Установить получателя"""
        self.recipient = recipient
        return self

    def set_print(self, print_type: str):
        """Установить необходимость печатной формы"""
        self.print = print_type
        return self

    def set_comment(self, comment: str):
        """Установить комментарий"""
        self.comment = comment
        return self

    def get_number(self) -> str:
        """Получить номер заказа"""
        return self.number

    def get_tariff_code(self) -> int:
        """Получить код тарифа"""
        return self.tariff_code

    def get_sender(self):
        """Получить отправителя"""
        return self.sender

    def get_recipient(self):
        """Получить получателя"""
        return self.recipient

    def get_comment(self):
        """Получить комментарий"""
        return self.comment

    @classmethod
    def with_order_uuid(cls, uuid: str):
        """Экспресс-метод: создать Order с UUID"""
        instance = cls()
        instance.uuid = uuid
        return instance

    @classmethod
    def with_cdek_number(cls, cdek_number: str):
        """Экспресс-метод: создать Order с номером CDEK"""
        instance = cls()
        instance.cdek_number = cdek_number
        return instance

