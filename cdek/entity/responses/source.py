from dataclasses import dataclass, fields
from typing import get_args, get_origin


@dataclass
class Source:
    """Базовый класс для всех классов ответов"""

    def get_dataclass_fields(self) -> dict[str, type]:
        return {f.name for f in fields(self)}

    def __setattr__(self, key, value):
        # Получаем описание поля (если оно есть)
        if key not in self.get_dataclass_fields():
            return
        flds = {f.name: f.type for f in fields(self)}

        # Если поле определено в dataclass, обрабатываем его тип
        if key in flds:
            expected_type = flds[key]
            origin = get_origin(expected_type)

            # ✅ Если это список других dataclass
            if origin is list or origin is list:
                inner_type = get_args(expected_type)[0]
                if isinstance(value, list) and hasattr(
                    inner_type, "__dataclass_fields__"
                ):
                    value = [
                        inner_type(**v) if isinstance(v, dict) else v for v in value
                    ]

            # ✅ Если это dataclass
            elif hasattr(expected_type, "__dataclass_fields__") and isinstance(
                value, dict
            ):
                value = expected_type(**value)

            # Устанавливаем через super() для dataclass полей
            super().__setattr__(key, value)
        else:
            # Для неизвестных полей используем object.__setattr__
            object.__setattr__(self, key, value)
