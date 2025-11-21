from __future__ import annotations

from typing import Optional

from pydantic import Field

from ..request import BaseRequest
from .item import Item


class CalcPackage(BaseRequest):
    weight: Optional[int] = Field(None, description="Вес упаковки в граммах")
    length: Optional[int] = Field(None, description="Длина упаковки в сантиметрах")
    width: Optional[int] = Field(None, description="Ширина упаковки в сантиметрах")
    height: Optional[int] = Field(None, description="Высота упаковки в сантиметрах")


class Package(CalcPackage):
    number: str = Field(..., description="Номер упаковки")
    weight: int = Field(..., description="Вес упаковки в граммах")
    commnet: Optional[str] = Field(None, description="Комментарий к упаковке")
    items: Optional[list[Item]] = Field(None, description="Позиции товаров в упаковке")
    package_id: Optional[str] = Field(
        None, description="Уникальный номер упаковки в ИС СДЭК"
    )

    def add_item(self, **kwargs):
        """Добавить товар в упаковку и вернуть созданный объект"""
        item = Item(**kwargs)
        if self.items is None:
            self.items = []
        self.items.append(item)
        return item
