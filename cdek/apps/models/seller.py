from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, Field


class Seller(BaseModel):
    """Модель для реквизитов истинного продавца"""

    name: Optional[str] = Field(None, description="Наименование истинного продавца")
    inn: Optional[str] = Field(None, description="ИНН истинного продавца")
    phone: Optional[str] = Field(None, description="Телефон истинного продавца")
    ownership_form: Optional[int] = Field(None, description="Код формы собственности")
    address: Optional[str] = Field(None, description="Адрес истинного продавца")
