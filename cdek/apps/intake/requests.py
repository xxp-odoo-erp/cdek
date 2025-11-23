from __future__ import annotations

from typing import Optional

from pydantic import Field

from ..models.intakes import Intakes
from ..request import BaseRequest


class IntakeRequest(BaseRequest, Intakes):
    lunch_time_from: Optional[str] = Field(None, description="Время начала обеда")
    lunch_time_to: Optional[str] = Field(None, description="Время окончания обеда")
