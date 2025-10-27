"""
Исключение ошибки авторизации в API CDEK
"""

from .cdek_exception import CdekException


class CdekAuthException(CdekException):
    """Ошибка авторизации в API CDEK"""

    def __init__(self, message):
        super().__init__(message)

