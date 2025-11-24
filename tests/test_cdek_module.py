from __future__ import annotations

import pytest

import cdek
from cdek.apps.agreement import AgreementApp
from cdek.apps.check import CheckApp
from cdek.apps.currency import CurrencyApp
from cdek.apps.form import BarcodeApp, InvoiceApp
from cdek.apps.intake import IntakeApp
from cdek.apps.location import LocationApp
from cdek.apps.office import OfficeApp
from cdek.apps.order import OrderApp
from cdek.apps.payment import PaymentApp
from cdek.apps.tariff import TariffApp
from cdek.apps.webhook import WebhookApp
from cdek.client import CdekClient


def test_public_api_exports_expected_names() -> None:
    expected_symbols = {
        "CdekClient",
        "CdekException",
        "CdekAuthException",
        "CdekRequestException",
        "constants",
    }

    for symbol in expected_symbols:
        assert symbol in cdek.__all__
        assert hasattr(cdek, symbol)


def test_client_initializes_test_account_defaults() -> None:
    client = CdekClient("TEST")

    assert client.base_url == "https://api.edu.cdek.ru/v2/"
    assert client.account == "wqGwiQx0gg8mLtiEKsUinjVSICCjtTEP"
    assert client.secure == "RmAmgvSgSl1yirlz9QupbzOJVqhCxcP5"
    assert client.account_type == "TEST"
    assert client.timeout == 5.0


def test_client_initializes_combat_account() -> None:
    client = CdekClient("login", secure="secret", timeout=10)

    assert client.base_url == "https://api.cdek.ru/v2/"
    assert client.account == "login"
    assert client.secure == "secret"
    assert client.account_type == "COMBAT"
    assert client.timeout == 10


def test_set_memory_stores_values_and_returns_self() -> None:
    client = CdekClient("login", secure="secret")
    memory = {"expires_in": 1, "access_token": "abc"}

    def callback(value: dict[str, str]) -> None:
        del value  # избегаем предупреждений

    returned = client.set_memory(memory, callback)

    assert returned is client
    assert client.memory is memory
    assert client.memory_save_callback is callback


@pytest.mark.parametrize(
    ("attribute", "expected_cls"),
    [
        ("currency", CurrencyApp),
        ("office", OfficeApp),
        ("order", OrderApp),
        ("location", LocationApp),
        ("tariff", TariffApp),
        ("barcode", BarcodeApp),
        ("invoice", InvoiceApp),
        ("payment", PaymentApp),
        ("agreement", AgreementApp),
        ("intake", IntakeApp),
        ("check", CheckApp),
        ("webhook", WebhookApp),
    ],
)
def test_client_app_properties(attribute: str, expected_cls: type) -> None:
    client = CdekClient("login", secure="secret")

    app = getattr(client, attribute)

    assert isinstance(app, expected_cls)
    assert app.client is client  # type: ignore


def test_test_account_exposes_all_apps_in_test_mode(test_client: CdekClient) -> None:
    expected_apps = [
        test_client.currency,
        test_client.office,
        test_client.order,
        test_client.location,
        test_client.tariff,
        test_client.barcode,
        test_client.invoice,
        test_client.payment,
        test_client.agreement,
        test_client.intake,
        test_client.check,
        test_client.webhook,
    ]

    for app in expected_apps:
        assert app.client.account_type == "TEST"
        assert app.client.base_url == "https://api.edu.cdek.ru/v2/"
