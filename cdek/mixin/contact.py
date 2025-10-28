from dataclasses import dataclass, field
from typing import TYPE_CHECKING
from ..entity.requests.phone import Phone

if TYPE_CHECKING:
    from ..entity.requests.phone import Phone

@dataclass
class Contact:
    """Trait для работы с контактной информацией"""

    company: str | None = None
    name: str | None = None
    email: str | None = None
    phones: 'list[Phone]' = field(default_factory=list)
    passport_series: str | None = None
    passport_number: str | None = None
    passport_date_of_issue: str | None = None
    passport_organization: str | None = None
    passport_date_of_birth: str | None = None
    tin: str | None = None

    def add_phone(self, number: str, additional: str | None = None):
        if self.phones is None:
            self.phones = []
        self.phones.append(Phone(number=number, additional=additional))
        return self

    def set_phones(self, number: str, additional: str | None = None):
        if self.phones is None:
            self.phones = []
        self.phones.append(Phone(number=number, additional=additional))
        return self

    def set_passport(self, passport_series: str, passport_number: str, passport_date_of_issue: str, passport_organization: str, passport_date_of_birth: str):
        self.passport_series = passport_series
        self.passport_number = passport_number
        self.passport_date_of_issue = passport_date_of_issue
        self.passport_organization = passport_organization
        self.passport_date_of_birth = passport_date_of_birth
        return self

    def set_tin(self, tin: str):
        """Установить ИНН получателя (только для международных заказов)"""
        self.tin = tin
        return self

    def set_name(self, name: str):
        """Установить имя"""
        self.name = name
        return self

    def set_company(self, company: str):
        """Установить название компании"""
        self.company = company
        return self

    def set_email(self, email: str):
        """Установить email"""
        self.email = email
        return self
