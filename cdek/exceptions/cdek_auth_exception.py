from .cdek_exception import CdekException


class CdekAuthException(CdekException):
    """Ошибка авторизации в API CDEK"""

    def __init__(self, message):
        """Сохранить сообщение об ошибке авторизации"""
        super().__init__(message)

