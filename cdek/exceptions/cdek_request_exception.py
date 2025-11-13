from .cdek_exception import CdekException


class CdekRequestException(CdekException):
    """Ошибка запроса к API CDEK"""

    def __init__(self, message, status_code=None):
        """Инициализировать исключение с сообщением и HTTP-статусом"""
        super().__init__(message)
        self.status_code = status_code

    @staticmethod
    def get_translation(code, message):
        """Получить перевод ошибки"""
        # Импортируем constants локально, чтобы избежать циклического импорта
        from .. import constants
        if code in constants.ERRORS:
            return f"{constants.ERRORS[code]}. {message}"
        return message

