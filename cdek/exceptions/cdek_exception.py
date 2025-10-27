class CdekException(Exception):
    """Базовое исключение для CDEK"""

    @staticmethod
    def get_translation(code, message):
        """Получить перевод ошибки"""
        # Импортируем constants локально, чтобы избежать циклического импорта
        from .. import constants
        if code in constants.ERRORS:
            return f"{constants.ERRORS[code]}. {message}"
        return message

