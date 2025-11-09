from __future__ import annotations

from pydantic import Field

from ..request import BaseRequest
from .item import Item


class CalcPackage(BaseRequest):
    weight: int | None = Field(None, description="Вес упаковки в граммах")
    length: int | None = Field(None, description="Длина упаковки в сантиметрах")
    width: int | None = Field(None, description="Ширина упаковки в сантиметрах")
    height: int | None = Field(None, description="Высота упаковки в сантиметрах")


class Package(CalcPackage):
    number: str = Field(..., description="Номер упаковки")
    weight: int = Field(..., description="Вес упаковки в граммах")
    commnet: str | None = Field(None, description="Комментарий к упаковке")
    items: list[Item] | None = Field(None, description="Позиции товаров в упаковке")
    package_id: str | None = Field(
        None, description="Уникальный номер упаковки в ИС СДЭК"
    )

    def add_item(self, **kwargs):
        item = Item(**kwargs)
        if self.items is None:
            self.items = []
        self.items.append(item)
        return item
