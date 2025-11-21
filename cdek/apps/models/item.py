from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, Field

from .money import Money
from .seller import Seller


class Item(BaseModel):
    name: str = Field(..., description="Название товара")
    ware_key: str = Field(..., description="Артикул товара")
    marking: Optional[str] = Field(None, description="Маркировка товара")
    payment: Money = Field(..., description="Сумма оплаты с НДС")
    weight: int = Field(..., description="Вес товара в граммах")
    weight_gross: Optional[int] = Field(None, description="Вес брутто")
    amount: int = Field(..., description="Количество товара")
    name_i18n: Optional[str] = Field(None, description="Название товара на другом языке")
    brand: Optional[str] = Field(None, description="Бренд на иностранном языке")
    country_code: Optional[str] = Field(
        None, description="Код страны производителя товара в формате ISO_3166-1_alpha-2"
    )
    material: Optional[int] = Field(None, description="Материал товара")
    wifi_gsm: Optional[bool] = Field(None, description="Признак наличия WiFi и GSM модема")
    url: Optional[str] = Field(None, description="URL товара")
    seller: Optional[Seller] = Field(None, description="Реквизиты истинного продавца")
    cost: float = Field(..., description="Стоимость товара")
    feacn_code: Optional[str] = Field(None, description="Код ТН ВЭД")
    jewel_uin: Optional[str] = Field(None, description="УИН ювелирного изделия")
    used_goods: Optional[bool] = Field(
        None, description="Признак товара б/у, применим для c2c заказов"
    )
