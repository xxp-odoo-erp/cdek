from __future__ import annotations

from pydantic import BaseModel, Field

from .money import Money
from .seller import Seller


class Item(BaseModel):
    name: str = Field(..., description="Название товара")
    ware_key: str = Field(..., description="Артикул товара")
    marking: str | None = Field(None, description="Маркировка товара")
    payment: Money = Field(..., description="Сумма оплаты с НДС")
    weight: int = Field(..., description="Вес товара в граммах")
    weight_gross: int | None = Field(None, description="Вес брутто")
    amount: int = Field(..., description="Количество товара")
    name_i18n: str | None = Field(None, description="Название товара на другом языке")
    brand: str | None = Field(None, description="Бренд на иностранном языке")
    country_code: str | None = Field(
        None, description="Код страны производителя товара в формате ISO_3166-1_alpha-2"
    )
    material: int | None = Field(None, description="Материал товара")
    wifi_gsm: bool | None = Field(None, description="Признак наличия WiFi и GSM модема")
    url: str | None = Field(None, description="URL товара")
    seller: Seller | None = Field(None, description="Реквизиты истинного продавца")
    cost: float = Field(..., description="Стоимость товара")
    feacn_code: str | None = Field(None, description="Код ТН ВЭД")
    jewel_uin: str | None = Field(None, description="УИН ювелирного изделия")
    used_goods: bool | None = Field(
        None, description="Признак товара б/у, применим для c2c заказов"
    )
