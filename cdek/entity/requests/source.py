"""
Базовый класс для всех запросов
"""

from typing import Dict, Any
from dataclasses import dataclass
from dataclasses import is_dataclass, fields
from enum import Enum
@dataclass
class Source:
    """Базовый класс для всех классов запросов"""

    pattern: list | None = None

    def prepare_request(self) -> Dict[str, Any]:
        """
        Формирует словарь параметров для запроса.
        Удаляет пустые значения.
        """
        # Если pattern установлен, используем его как маску
        if self.pattern:
            entity_vars = self.pattern
        else:
            entity_vars = vars(self)

        dynamic = {}

        # Если pattern - это список, то просто собираем все параметры
        if isinstance(entity_vars, list):
            dynamic = {}
            for attr_name in entity_vars:
                value = getattr(self, attr_name, None)
                if value is not None:
                    dynamic[attr_name] = value
            return dynamic

        for key, val in entity_vars.items():
            if val is None:
                continue

            value = getattr(self, key, None)
            if value is None:
                continue

            if isinstance(value, list):
                dynamic[key] = []
                for item in value:
                    if hasattr(item, 'prepare_request'):
                        item_dict = item.prepare_request()
                        if item_dict:
                            dynamic[key].append(item_dict)
                    elif hasattr(item, '__dict__'):
                        item_dict = vars(item)
                        item_dict_null_filtered = {k: v for k, v in item_dict.items() if v is not None}
                        if item_dict_null_filtered:
                            dynamic[key].append(item_dict_null_filtered)
                    elif item is not None:
                        dynamic[key].append(item)
            elif hasattr(value, 'prepare_request'):
                dynamic[key] = value.prepare_request()
            elif hasattr(value, '__dict__'):
                item_dict = vars(value)
                dynamic[key] = {k: v for k, v in item_dict.items() if v is not None}
            else:
                dynamic[key] = value

        return dynamic


def asdict_ex(obj: Any, exclude_none: bool = True) -> dict[str, Any]:
    """
    Рекурсивно преобразует dataclass в dict, исключая:
      - поля с metadata['exclude'] == True
      - поля, которые не установлены
      - поля со значением None (если exclude_none=True)
    Поддерживает Enum: сохраняет .value

    Args:
        obj: Dataclass объект для преобразования
        exclude_none: Если True, исключает поля со значением None

    Returns:
        dict: Словарь с преобразованными данными
    """
    if not is_dataclass(obj):
        raise TypeError(f"asdict_ex ожидает dataclass, а не {type(obj)}")

    result = {}
    for f in fields(obj):
        if f.metadata.get("exclude", False):
            continue
        if not hasattr(obj, f.name):
            continue

        value = getattr(obj, f.name)

        # Исключаем None значения если exclude_none=True
        if exclude_none and value is None:
            continue

        # Обработка Enum
        if isinstance(value, Enum):
            result[f.name] = value.value
        # Рекурсивно обрабатываем вложенные dataclass'ы
        elif is_dataclass(value):
            result[f.name] = asdict_ex(value, exclude_none=exclude_none)
        # Списки / словари
        elif isinstance(value, list):
            # Исключаем пустые списки если exclude_none=True
            if exclude_none and len(value) == 0:
                continue
            result[f.name] = [
                asdict_ex(v, exclude_none=exclude_none)
                if is_dataclass(v)
                else (v.value if isinstance(v, Enum) else v)
                for v in value
            ]
        elif isinstance(value, dict):
            # Исключаем пустые словари если exclude_none=True
            if exclude_none and len(value) == 0:
                continue
            result[f.name] = {
                k: asdict_ex(v, exclude_none=exclude_none)
                if is_dataclass(v)
                else (v.value if isinstance(v, Enum) else v)
                for k, v in value.items()
            }
        else:
            result[f.name] = value

    return result
