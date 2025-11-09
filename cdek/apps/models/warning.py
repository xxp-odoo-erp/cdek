from pydantic import BaseModel, Field


class Warning(BaseModel):
    """Предупреждения"""

    code: str | None = Field(None, description="Код предупреждения")
    message: str | None = Field(None, description="Описание предупреждения")
