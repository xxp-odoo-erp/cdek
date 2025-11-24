from .. import constants


class CdekException(Exception):
    """Базовое исключение для CDEK"""

    @staticmethod
    def get_translation(code: str, message: str) -> str:
        """Получить перевод ошибки"""
        if code in constants.ERRORS:
            return f"{constants.ERRORS[code]}. {message}"
        return message
