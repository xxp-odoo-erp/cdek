from __future__ import annotations

from typing import Literal

from pydantic import Field

from ..models.print import PrintForm, PrintType


class PrintBarcodeRequest(PrintForm):
    format: Literal["A4", "A5", "A6", "A7"] = Field("A4", description="Формат печати")
    lang: Literal["RUS", "ENG"] = Field("RUS", description="Язык печати")


class PrintInvoiceRequest(PrintForm):
    type: PrintType | None = Field(None, description="Тип накладной")
