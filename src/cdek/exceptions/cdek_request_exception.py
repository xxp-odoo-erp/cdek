from typing import Any

from .. import constants
from .cdek_exception import CdekException


class CdekRequestException(CdekException):
    """Ошибка запроса к API CDEK"""

    def __init__(
        self, message: str, status_code: int | None = None, response: Any | None = None
    ):
        """Инициализировать исключение с сообщением и HTTP-статусом"""
        super().__init__(message)
        self.status_code = status_code
        self.response = response

    @staticmethod
    def get_translation(code: str, message: str) -> str:
        """Получить перевод ошибки"""
        if code in constants.ERRORS:
            return f"{constants.ERRORS[code]}. {message}"
        return message
