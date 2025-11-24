from __future__ import annotations

from collections.abc import Callable
from typing import Any

from .apps.agreement import AgreementApp
from .apps.check import CheckApp
from .apps.currency import CurrencyApp
from .apps.form import BarcodeApp, InvoiceApp
from .apps.intake import IntakeApp
from .apps.location import LocationApp
from .apps.office import OfficeApp
from .apps.order import OrderApp
from .apps.payment import PaymentApp
from .apps.tariff import TariffApp
from .apps.webhook import WebhookApp


class CdekClient:
    """Клиент взаимодействия с API CDEK 2.0"""

    def __init__(self, account: str, secure: str | None = None, timeout: float = 5.0):
        """
        Конструктор клиента

        Args:
            account: Логин Account в сервисе Интеграции
            secure: Пароль Secure password в сервисе Интеграции
            timeout: Настройка клиента задающая общий тайм-аут запроса в секундах
        """
        if account == "TEST":
            self.base_url: str = "https://api.edu.cdek.ru/v2/"
            self.account: str = "wqGwiQx0gg8mLtiEKsUinjVSICCjtTEP"
            self.secure: str | None = "RmAmgvSgSl1yirlz9QupbzOJVqhCxcP5"
            self.account_type: str = "TEST"
        else:
            self.base_url = "https://api.cdek.ru/v2/"
            self.account = account
            self.secure = secure
            self.account_type = "COMBAT"

        self.timeout: float = timeout
        self.token: str | None = None
        self.expire: int = 0
        self.memory: dict[str, Any] | None = None
        self.memory_save_callback: Callable[[dict[str, Any]], None] | None = None

    def set_memory(
        self,
        memory: dict[str, Any] | None,
        save_callback: Callable[[dict[str, Any]], None],
    ) -> CdekClient:
        """
        Установить параметры сохранения токена

        Args:
            memory: массив настройки сохранения
            save_callback: коллбэк сохранения

        Returns:
            self
        """
        self.memory = memory
        self.memory_save_callback = save_callback
        return self

    @property
    def currency(self) -> CurrencyApp:
        """Получение информации о валюте"""
        return CurrencyApp(self)

    @property
    def office(self) -> OfficeApp:
        """Получение информации о ПВЗ"""
        return OfficeApp(self)

    @property
    def order(self) -> OrderApp:
        """Получение информации о заказе"""
        return OrderApp(self)

    @property
    def location(self) -> LocationApp:
        """Получение информации о местоположении"""
        return LocationApp(self)

    @property
    def tariff(self) -> TariffApp:
        """Получение информации о тарифе"""
        return TariffApp(self)

    @property
    def barcode(self) -> BarcodeApp:
        """Получение информации о штрих-коде"""
        return BarcodeApp(self)

    @property
    def invoice(self) -> InvoiceApp:
        """Получение информации о накладной"""
        return InvoiceApp(self)

    @property
    def payment(self) -> PaymentApp:
        """Получение информации о платеже"""
        return PaymentApp(self)

    @property
    def agreement(self) -> AgreementApp:
        """Получение информации о договоренности"""
        return AgreementApp(self)

    @property
    def intake(self) -> IntakeApp:
        """Получение информации о заявке на вызов курьера"""
        return IntakeApp(self)

    @property
    def check(self) -> CheckApp:
        """Получение информации о чеке"""
        return CheckApp(self)

    @property
    def webhook(self) -> WebhookApp:
        """Получение информации о вебхуке"""
        return WebhookApp(self)
