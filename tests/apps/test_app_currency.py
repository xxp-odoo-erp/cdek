from __future__ import annotations


def test_currency_app_knows_supported_codes(test_client) -> None:  # type: ignore
    codes = test_client.currency.all()

    assert isinstance(codes, list)
    assert 1 in codes  # RUB должен присутствовать
    assert test_client.currency.get("RUB") == 1
