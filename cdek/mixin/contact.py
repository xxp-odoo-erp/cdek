from dataclasses import dataclass, field
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..requests.phone import Phone

@dataclass
class ContactMixin:
    """Mixin for working with contact information."""

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
        """Add a phone number."""
        from ..requests.phone import Phone  # noqa
        if self.phones is None:
            self.phones = []
        self.phones.append(Phone(number=number, additional=additional))
        return self

    def set_phones(self, number: str, additional: str | None = None):
        """Set phone numbers."""
        from ..requests.phone import Phone  # noqa
        if self.phones is None:
            self.phones = []
        self.phones.append(Phone(number=number, additional=additional))
        return self

    def set_passport(self, passport_series: str, passport_number: str, passport_date_of_issue: str, passport_organization: str, passport_date_of_birth: str):
        """Set passport information."""
        self.passport_series = passport_series
        self.passport_number = passport_number
        self.passport_date_of_issue = passport_date_of_issue
        self.passport_organization = passport_organization
        self.passport_date_of_birth = passport_date_of_birth
        return self

    def set_tin(self, tin: str):
        """Set taxpayer identification number (TIN) for international orders."""
        self.tin = tin
        return self

    def set_name(self, name: str):
        """Set contact name."""
        self.name = name
        return self

    def set_company(self, company: str):
        """Set company name."""
        self.company = company
        return self

    def set_email(self, email: str):
        """Set email address."""
        self.email = email
        return self
