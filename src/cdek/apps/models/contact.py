from __future__ import annotations

from datetime import date as Date
from enum import Enum

from pydantic import BaseModel, Field, field_serializer

from .phone import Phone


class ContragentType(str, Enum):
    LEGAL_ENTITY = "LEGAL_ENTITY"
    INDIVIDUAL = "INDIVIDUAL"


class Tin(BaseModel):
    tin: str | None = Field(None, max_length=255, description="ИНН")


class Passport(BaseModel):
    passport_series: str | None = Field(
        None, max_length=255, description="Серия паспорта"
    )
    passport_number: str | None = Field(
        None, max_length=255, description="Номер паспорта"
    )
    passport_date_of_issue: Date | None = Field(
        None, description="Дата выдачи паспорта"
    )
    passport_organization: str | None = Field(
        None, max_length=255, description="Организация выдавшая паспорт"
    )
    passport_date_of_birth: Date | None = Field(None, description="Дата рождения")

    @field_serializer("passport_date_of_issue")
    def serialize_passport_date_of_issue(self, passport_date_of_issue: Date) -> str:
        """Вернуть дату выдачи паспорта в формате YYYY-MM-DD"""
        return passport_date_of_issue.strftime("%Y-%m-%d")

    @field_serializer("passport_date_of_birth")
    def serialize_passport_date_of_birth(self, passport_date_of_birth: Date) -> str:
        """Вернуть дату рождения в формате YYYY-MM-DD"""
        return passport_date_of_birth.strftime("%Y-%m-%d")


class Contact(Passport, Tin):
    company: str | None = Field(None, description="Название компании")
    name: str | None = Field(None, description="Имя заказчика")
    contragent_type: ContragentType | None = Field(None, description="Тип контрагента")
    email: str | None = Field(None, description="Email")
    phones: list[Phone] = Field(default_factory=list, description="Телефоны")

    def add_phone(self, number: str, additional: str | None = None) -> Contact:
        """Добавить новый номер телефона в контакт"""
        phone = Phone(number=number, additional=additional)
        self.phones.append(phone)
        return self
