from pydantic import BaseModel, Field


class Image(BaseModel):
    number: int | None
    url: str = Field(..., max_length=255, description="Ссылка на фото")
