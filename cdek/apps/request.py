from pydantic import BaseModel


class BaseRequest(BaseModel):
    """Модель запроса"""

    @classmethod
    def init(cls, **kwargs):
        """Инициализация запроса"""
        return cls(**kwargs)
