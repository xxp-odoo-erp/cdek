from __future__ import annotations

from pydantic import Field

from ..models.intakes import Intakes


class IntakeRequest(Intakes):
    lunch_time_from: str | None = Field(default=None, description="Время начала обеда")  # type: ignore
    lunch_time_to: str | None = Field(default=None, description="Время окончания обеда")  # type: ignore
