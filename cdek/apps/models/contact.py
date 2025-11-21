from __future__ import annotations

from typing import Optional

from datetime import date as Date
from enum import Enum

from pydantic import BaseModel, Field, field_serializer

from ..request import BaseRequest
from .phone import Phone


class ContragentType(str, Enum):
    LEGAL_ENTITY = "LEGAL_ENTITY"
    INDIVIDUAL = "INDIVIDUAL"


class Tin(BaseModel):
    tin: Optional[str] = Field(None, max_length=255, description="ИНН")


class Passport(BaseModel):
    passport_series: Optional[str] = Field(
        None, max_length=255, description="Серия паспорта"
    )
    passport_number: Optional[str] = Field(
        None, max_length=255, description="Номер паспорта"
    )
    passport_date_of_issue: Optional[Date] = Field(
        None, description="Дата выдачи паспорта"
    )
    passport_organization: Optional[str] = Field(
        None, max_length=255, description="Организация выдавшая паспорт"
    )
    passport_date_of_birth: Optional[Date] = Field(None, description="Дата рождения")

    @field_serializer("passport_date_of_issue")
    def serialize_passport_date_of_issue(self, passport_date_of_issue: Date) -> str:
        """Вернуть дату выдачи паспорта в формате YYYY-MM-DD"""
        return passport_date_of_issue.strftime("%Y-%m-%d")

    @field_serializer("passport_date_of_birth")
    def serialize_passport_date_of_birth(self, passport_date_of_birth: Date) -> str:
        """Вернуть дату рождения в формате YYYY-MM-DD"""
        return passport_date_of_birth.strftime("%Y-%m-%d")


class Contact(BaseRequest, Passport, Tin):
    company: Optional[str] = Field(None, description="Название компании")
    name: Optional[str] = Field(None, description="Имя заказчика")
    contragent_type: Optional[ContragentType] = Field(None, description="Тип контрагента")
    email: Optional[str] = Field(None, description="Email")
    phones: list[Phone] = Field(default_factory=list, description="Телефоны")

    def add_phone(self, number: str, additional: Optional[str] = None):
        """Добавить новый номер телефона в контакт"""
        phone = Phone(number=number, additional=additional)
        if self.phones is None:
            self.phones = []
        self.phones.append(phone)
        return self
