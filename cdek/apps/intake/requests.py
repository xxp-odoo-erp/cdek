from pydantic import Field

from ..models.intakes import Intakes
from ..request import BaseRequest


class IntakeRequest(BaseRequest, Intakes):
    lunch_time_from: str | None = Field(None, description="Время начала обеда")
    lunch_time_to: str | None = Field(None, description="Время окончания обеда")
