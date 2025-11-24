from __future__ import annotations

from pydantic import BaseModel, Field


class Seller(BaseModel):
    """Модель для реквизитов истинного продавца"""

    name: str | None = Field(None, description="Наименование истинного продавца")
    inn: str | None = Field(None, description="ИНН истинного продавца")
    phone: str | None = Field(None, description="Телефон истинного продавца")
    ownership_form: int | None = Field(None, description="Код формы собственности")
    address: str | None = Field(None, description="Адрес истинного продавца")
