from __future__ import annotations

from typing import Optional

from typing import Literal

from pydantic import Field

from ..models.print import PrintForm, PrintType
from ..request import BaseRequest


class PrintBarcodeRequest(BaseRequest, PrintForm):
    format: Literal["A4", "A5", "A6", "A7"] = Field("A4", description="Формат печати")
    lang: Literal["RUS", "ENG"] = Field("RUS", description="Язык печати")


class PrintInvoiceRequest(BaseRequest, PrintForm):
    type: Optional[PrintType] = Field(None, description="Тип накладной")
