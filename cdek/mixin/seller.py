from dataclasses import dataclass

@dataclass
class Seller:
    name: str | None = None
    inn: str | None = None
    phone: str | None = None
    ownership_form: int | None = None
    address: str | None = None
